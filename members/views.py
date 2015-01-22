from django.http import JsonResponse
from django.views import generic
from members.models import AuthUserActivity, AuthUser, \
	AuthUserCart, AuthUserOrder, AuthUserOrderItem, AuthUserAddress, RegistrationProfile
from goods.models import Product
from members.forms import CustomAuthenticationForm, RegistrationForm
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import stripe
from django.shortcuts import redirect
from django.conf import settings
import logging
from datetime import datetime, timedelta
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from registration.backends.default.views import ActivationView as BaseActivationView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login
from registration import signals
from django.contrib.sites.models import RequestSite, Site


logger = logging.getLogger(__name__)

class ClosetView(generic.ListView):
	template_name = 'members/closet/closet.html'
	context_object_name = 'saved_items'
	model = AuthUserActivity

class ActivationView(BaseActivationView):
	
	def activate(self, request, activation_key):
		"""Log user in upon successful activation"""
		activated_user = super(ActivationView, self).activate(self, request, activation_key)
		login(request, activated_user)
		return activated_user
	

class SignupView(BaseRegistrationView):

	template_name = 'registration/registration_form.html'
	form_class = RegistrationForm
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(SignupView, self).get_context_data(**kwargs)
		context['signup_form'] = RegistrationForm()
		context['login_form'] = RegistrationForm()

		# TODO: do not add 'site_name' to context
		# once the 'sites' are setup in settings
		context['site_name'] = settings.SITE_NAME
		return context

	def register(self, request, **cleaned_data):
		email, password = cleaned_data['email'], cleaned_data['password']
		if Site._meta.installed:
			site = Site.objects.get_current()
		else:
			site = RequestSite(request)
		new_user = RegistrationProfile.objects.create_inactive_user(
			email, password, site,
			send_email=self.SEND_ACTIVATION_EMAIL,
			request=request,
		)
		signals.user_registered.send(sender=self.__class__,
									 user=new_user,
									 request=request)		
		return new_user


def ProductLike(request):
	"""Adds product instance to 'saved_items' field of 
		AuthUserActivity model
	"""
	
	# because this is called via AJAX, the @login_required decorator
	# is not very useful, so instead we have to manually check if
	# user is authenticated or not and return appropariate status in json
	if(not request.user.is_authenticated()):
		return JsonResponse('loginrequired', safe=False)
	
	if request.method == "POST":
		userinstance = request.user
		product = Product.objects.get(pk=int(request.POST['id']))
		useractivity = AuthUserActivity.objects.get(authuser=userinstance)
		if product in useractivity.saved_items.all():
			useractivity.saved_items.remove(product)
		else:
			useractivity.saved_items.add(product)
		useractivity.save()
		return JsonResponse('success', safe=False)
	else:
		return JsonResponse('success', safe=False)

@login_required
def AddToCart(request):

	if request.method == "POST" and request.is_ajax:
		userinstance = request.user
		product = Product.objects.get(pk=int(request.POST['id']))
		usercart, created = AuthUserCart.objects.get_or_create(authuser=userinstance)
		usercart.saved_items.add(product)
		usercart.save()
		count = usercart.get_item_count()
		return JsonResponse({'count': count, 'message':'success'})
	else:
		return JsonResponse('success', safe=False)

@login_required
def RemoveFromCart(request):

	if request.method == "POST" and request.is_ajax:
		userinstance = request.user
		product = Product.objects.get(pk=int(request.POST['id']))
		usercart = AuthUserCart.objects.get(authuser=userinstance)
		usercart.saved_items.remove(product)
		usercart.save()
		count = usercart.get_item_count()
		total = usercart.get_cart_total()
		return JsonResponse({'count': count, 'total': total, 'id':product.id})
	else:
		return JsonResponse('success', safe=False)

class CartView(LoginRequiredMixin, generic.DetailView):
	template_name = 'members/purchase/cart.html'
	context_object_name = 'cart'
	model = AuthUserCart

	def get_object(self, queryset=None):
		return AuthUserCart.objects.get(authuser=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(CartView, self).get_context_data(**kwargs)
		context['FEATURE_NAME_BUYANDTRY'] = settings.FEATURE_NAME_BUYANDTRY
		context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

		# TODO: do not add 'site_name' to context
		# once the 'sites' are setup in settings
		context['site_name'] = settings.SITE_NAME
		return context

class CheckoutView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'members/purchase/checkout.html'

class CartCheckoutCallbackView(LoginRequiredMixin, generic.DetailView):
	template_name = 'members/purchase/cart.html'
	context_object_name = 'cart'
	model = AuthUserCart

	def get_object(self, queryset=None):
		return AuthUserCart.objects.get(authuser=self.request.user)

	def post(self, request, *args, **kwargs):
		try:
			# create new order
			order = AuthUserOrder()
			order.authuser = self.request.user
			order.save()
			logger.debug('Created new order %d' % order.id)

			cart = self.get_object()

			order_type = request.POST['order_type'].strip().lower()
			capture_order = (order_type == 'buy')

			# create charge with stripe,
			try:
				token_id = request.POST['token[id]']
				total_amount_in_cents = int(request.POST['total_amount'])

				if(total_amount_in_cents != cart.get_cart_total_in_cents()):
					# either cart has changed since payment or
					# user is trying something nasty
					# in any case we have a discrepancy between
					# what was shown to the user at the time of checkout
					# and current cart contents
					# it is best to stop right here and refresh the cart
					# so that user can checkout again
					logger.info('Cart total did not match the total that came in the request')
					return JsonResponse({'status': 'error', 'message': 'Total ammount does not match.'})

				order_type = request.POST['order_type']
				stripe.api_key = settings.STRIPE_SECRET_KEY
				stripe.Charge.create(
									amount=total_amount_in_cents,
									currency="usd",
									card=token_id,
									capture=capture_order,
									metadata={
											'order_id': order.id,
											'order_type': order_type
											})

	 		except Exception, e:
				logger.error('Error in CartCheckoutCallbackView.post()')
				logger.error(str(e))
				return JsonResponse({'status': 'error', 'message': 'Failed to charge credit card.'})

			# create or update shipping address
			#
			# TODO: allow multiple addresses per user
			# right now there is only one address per user which
			# is enforced in the database with a Unique key on user id
			shipping_address = None
			try:
				shipping_address = AuthUserAddress.objects.get(authuser=self.request.user)
				logger.debug('Updating existing shipping address')
			except AuthUserAddress.DoesNotExist:
				# no address, that's ok we will create a new one
				shipping_address = AuthUserAddress()
				logger.debug('Creating new shipping address')

			# TODO: shipping address should be tied to the order
			# right not it is only tied to user
			shipping_address.authuser = self.request.user
			shipping_address.street = request.POST['args[shipping_address_line1]']
			shipping_address.city = request.POST['args[shipping_address_city]']
			shipping_address.state = request.POST['args[shipping_address_state]']
			shipping_address.zipcd = request.POST['args[shipping_address_zip]']
			shipping_address.shipping = True
			shipping_address.save()

			# add items to order
			for product in cart.saved_items.all():
				order_item = AuthUserOrderItem()
				order_item.product = product
				order_item.order = order
				order_item.sell_price = product.current_price
				order_item.captured = capture_order
				if(capture_order):
					order_item.capture_time = datetime.now()
				else:
					order_item.capture_time = datetime.now() + timedelta(hours=settings.STRIPE_CAPTURE_TRANSACTION_TIME)
				order_item.quantity = 1
				order_item.save()
			logger.debug('Added items to order')

			# all items have been saved in the order now remove them from the cart
			# TODO: once the item is purchased the total available quantity should be adjusted
			# which we don't keep track of right now anywhere
			for product in cart.saved_items.all():
				cart.saved_items.remove(product)
				logger.debug('removing from cart %s' % str(order_item.product))
			cart.save()
			logger.debug('Removed items from cart')

			return JsonResponse({'status': 'ok', 'message': 'Order is completed.'})
		except Exception, e:
			logger.error('Error in CartCheckoutCallbackView.post()')
			logger.error(str(e))
			return JsonResponse({'status': 'error', 'message': 'Error processing the order.'})


def SubmitCustomerPayment(request):
	stripe.api_key = "sk_test_Ss8OxSVnDLbGv3qJ2HGUNNau"

	if request.method == "POST":
		token = request.POST['stripeToken']

		try:
		  charge = stripe.Charge.create(
		      amount=1000,  # amount in cents, again
		      currency="usd",
		      card=token,
		      description="payinguser@example.com"
		  )
		except stripe.CardError, e:
		  # The card has been declined
		  pass
		return redirect('members:review')
	return JsonResponse('not a post request homes', safe=False)


class ReviewView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'members/purchase/review.html'
