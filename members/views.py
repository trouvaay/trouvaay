from django.http import JsonResponse
from django.views import generic
from members.models import AuthUserActivity, AuthUser, \
    AuthUserCart, AuthUserOrder, AuthUserOrderItem, AuthUserAddress, RegistrationProfile, \
    PromotionOffer, PromotionRedemption
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
from helper import send_email_from_template, get_site
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render_to_response
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from decimal import Decimal

logger = logging.getLogger(__name__)

# TODO: For profile page
# class ProfileView(generic.ListView):
# template_name = 'members/closet/closet.html'
# context_object_name = 'saved_items'
# model = AuthUserActivity


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
        # context['signup_form'] = RegistrationForm()
        context['login_form'] = RegistrationForm()

        # TODO: do not add 'site_name' to context
        # once the 'sites' are setup in settings
        context['site_name'] = settings.SITE_NAME
        print ('this is template context',  context)
        return context

    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password']
        site = get_site(request)
        new_user = RegistrationProfile.objects.create_active_user(
            email, password, site,
            send_email=False,
            request=request,
        )
        user = authenticate(email=email, password=password)
        login(request, user)
        signals.user_activated.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user


class AjaxLoginView(generic.TemplateView):
    """Displays login/signup forms that can be loaded via ajax"""
    
    template_name = "members/auth/ajax_signup_login.html"
    
    def get_context_data(self, **kwargs):

        if(self.request.user.is_authenticated()):
            django_logout(self.request)

        context = super(AjaxLoginView, self).get_context_data(**kwargs)
        context['login_form'] = CustomAuthenticationForm()
        context['signup_form'] = RegistrationForm()
        return context
    

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


class ReserveCallbackView(generic.DetailView):
    context_object_name = 'product'
    model = Product

    def get_object(self):
        product_id = self.request.POST.get('product_id', None)
        if(not product_id):
            return None
        try:
            return Product.objects.get(pk=int(product_id))
        except Product.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        try:
            # create new order
            order = AuthUserOrder()

            product = self.get_object()

            order_type = request.POST['order_type'].strip().lower()
            capture_order = (order_type == 'buy')

            # create charge with stripe,
            try:
                token_id = request.POST['token[id]']
                total_amount_in_cents = int(request.POST['total_amount'])

                logger.debug('total_amount_in_cents %d' % total_amount_in_cents)

                discounts, subtotal_dollar_value, taxes, total = AuthUserOrder.compute_order_line_items(self.request.user, total_price_before_offers=product.current_price)

                logger.debug('discounts %s' % str(discounts))
                logger.debug('subtotal_dollar_value %s' % str(subtotal_dollar_value))
                logger.debug('total %s' % str(total))

                if(total_amount_in_cents != total['in_cents']):
                    # either product price has changed since payment or
                    # user is trying to do something nasty
                    # in any case we have a discrepancy between
                    # what was shown to the user at the time of checkout
                    # and current product prive
                    # it is best to stop right here and refresh the page
                    logger.info('Product price did not match the total that came in the request')
                    return JsonResponse({'status': 'error', 'message': 'Total ammount does not match.'})

                order_user = self.request.user
                is_existing = True
                if(not order_user.is_authenticated()):
                    email = self.request.POST.get('token[email]', None)
                    if(not email):
                        # cannot go any further without email
                        logger.info('No email in the request')
                        return JsonResponse({'status': 'error', 'message': 'No email'})
                    is_existing, order_user = get_user_model().get_user_by_email(email)
                    logger.debug('is_existing: %s' % str(is_existing))

                order.authuser = order_user
                order.taxes = taxes['dollar_value']
                order.save()
                logger.debug('Created new order %d' % order.id)

                # create redemptions
                for discount in discounts:

                    offer_id = discount['offer_id']
                    redemption = PromotionRedemption()
                    redemption.authuser = order_user
                    redemption.offer_id = offer_id
                    redemption.order = order
                    redemption.timestamp = timezone.now()
                    redemption.total_before_discount = product.current_price
                    redemption.discount_amount = discount['dollar_value']
                    redemption.save()

                    logger.debug('Created redemption %d' % redemption.id)

                stripe.api_key = settings.STRIPE_SECRET_KEY
                stripe.Charge.create(
                    amount=total_amount_in_cents,
                    currency="usd",
                    description=product.short_name,
                    card=token_id,
                    capture=capture_order,
                    receipt_email=order_user.email,
                    metadata={
                        'order_id': order.id,
                        'order_type': order_type
                        })

            except Exception, e:
                logger.error('Error in ReserveCallbackView.post()')
                logger.error(str(e))
                return JsonResponse({'status': 'error', 'message': 'Failed to charge credit card.'})

            # create or update shipping address
            #
            # TODO: allow multiple addresses per user
            # right now there is only one address per user which
            # is enforced in the database with a Unique key on user id
            shipping_address = None
            try:
                shipping_address = AuthUserAddress.objects.get(authuser=order_user)
                logger.debug('Updating existing shipping address')
            except AuthUserAddress.DoesNotExist:
                # no address, that's ok we will create a new one
                shipping_address = AuthUserAddress()
                logger.debug('Creating new shipping address')

            # TODO: shipping address should be tied to the order
            # right not it is only tied to user
            shipping_address.authuser = order_user
            shipping_address.street = request.POST['args[shipping_address_line1]']
            shipping_address.city = request.POST['args[shipping_address_city]']
            shipping_address.state = request.POST['args[shipping_address_state]']
            shipping_address.zipcd = request.POST['args[shipping_address_zip]']
            shipping_address.shipping = True
            shipping_address.save()

            # add item to order
            order_item = AuthUserOrderItem()
            order_item.product = product
            order_item.order = order
            order_item.sell_price = product.current_price
            order_item.captured = capture_order
            if(order_item.captured):
                order_item.capture_time = timezone.now()
            else:
                order_item.capture_time = timezone.now() + timedelta(hours=settings.STRIPE_CAPTURE_TRANSACTION_TIME)
            order_item.quantity = 1
            order_item.save()
            logger.debug('Added items to order')

            # send email with store address
            email_context = {
                             'product': product,
                             'site': get_site(self.request),
                             'capture_date': order_item.capture_time.date() if not order_item.captured else None
                             }

            if(not is_existing):
                # This is a newly created user without password. We will send this
                # user a password reset link along with the order
                # add extra context parameters needed for password reset link
                email_context['token'] = default_token_generator.make_token(order_user)
                email_context['uid'] = urlsafe_base64_encode(force_bytes(order_user.pk))
                email_context['domain'] = get_current_site(request).domain
                email_context['protocol'] = 'https' if self.request.is_secure() else 'http'

                
            send_email_from_template(to_email=order_user.email, context=email_context,
                subject_template='members/purchase/reserve_confirmation_email_subject.txt',
                plain_text_body_template='members/purchase/reserve_confirmation_email_body.txt',
                html_body_template='members/purchase/reserve_confirmation_email_body.html')


            return JsonResponse({
                'status': 'ok',
                'product_name': product.short_name,
                'image_src': product.productimage_set.first().image.build_url(width=200, height=200, crop="fit"),
                'store_name': product.store.retailer.short_name,
                'store_street': product.store.street,
                'store_street2': product.store.street2 if product.store.street2 else '',
                'store_city': product.store.city,
                'store_state': product.store.state,
                'store_zipcode': product.store.zipcd,
                'capture_date': order_item.capture_time.date() if not order_item.captured else None
            })
        except Exception, e:
            logger.error('Error in ReserveCallbackView.post()')
            logger.error(str(e))
            return JsonResponse({'status': 'error', 'message': 'Error processing the order.'})


class PreCheckoutView(generic.DetailView):
    context_object_name = 'product'
    model = Product

    def get_object(self):
        product_id = self.request.POST.get('product_id', None)
        if(not product_id):
            return None
        try:
            return Product.objects.get(pk=int(product_id))
        except Product.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):

        product = self.get_object()

        discounts, subtotal_dollar_value, taxes, total = AuthUserOrder.compute_order_line_items(user=self.request.user, total_price_before_offers=product.current_price)
        total_discount = 0
        for discount in discounts:
            total_discount += discount['dollar_value']
        capture_time = timezone.now() + timedelta(hours=settings.STRIPE_CAPTURE_TRANSACTION_TIME)
        stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        feature_name_reserve = settings.FEATURE_NAME_RESERVE
        site_name = settings.SITE_NAME
        return render_to_response('members/purchase/pre_checkout.html', locals())


def can_reserve(request):
    """Checks for permissions whether user is able to reserve a product.
    """
    
    if(request.user.is_authenticated()):
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'login_required'})
    

@sensitive_post_parameters()
@csrf_protect
@never_cache
def custom_login(request, template_name='registration/login.html',
          authentication_form=CustomAuthenticationForm):
    """This is a wrapper for django's login view.
    It allows us to pass "next" parameter properly.
    
    """

    # the foolowing unbound instances of forms are needed
    # only for rendering of the template by login 'GET'
    # the actual login 'POST' will be using authentication_form
    # from above
    extra_context = {
                     'login_form': CustomAuthenticationForm(),
                     'signup_form': RegistrationForm()
                     }
    if request.method == "GET":
        next_param = request.GET.get('next', None)
        if(next_param):
            extra_context = {
                             'login_form': CustomAuthenticationForm(initial={'next':next_param}),
                             'signup_form': RegistrationForm()
                             }

    return django_login(request=request,
                        template_name=template_name,
                        authentication_form=authentication_form,
                        extra_context=extra_context)


#########Unused Cart Feature ###################

# @login_required
# def AddToCart(request):

#     if request.method == "POST" and request.is_ajax:
#         userinstance = request.user
#         product = Product.objects.get(pk=int(request.POST['id']))
#         usercart, created = AuthUserCart.objects.get_or_create(authuser=userinstance)
#         usercart.saved_items.add(product)
#         usercart.save()
#         count = usercart.get_item_count()
#         return JsonResponse({'count': count, 'message':'success'})
#     else:
#         return JsonResponse('success', safe=False)
        
# class CheckoutView(LoginRequiredMixin, generic.TemplateView):
#     template_name = 'members/purchase/checkout.html'

# @login_required
# def RemoveFromCart(request):

#     if request.method == "POST" and request.is_ajax:
#         userinstance = request.user
#         product = Product.objects.get(pk=int(request.POST['id']))
#         usercart = AuthUserCart.objects.get(authuser=userinstance)
#         usercart.saved_items.remove(product)
#         usercart.save()
#         count = usercart.get_item_count()
#         total = usercart.get_cart_total()
#         return JsonResponse({'count': count, 'total': total, 'id':product.id})
#     else:
#         return JsonResponse('success', safe=False)


# class CartView(LoginRequiredMixin, generic.DetailView):
#     template_name = 'members/purchase/cart.html'
#     context_object_name = 'cart'
#     model = AuthUserCart

#     def get_object(self, queryset=None):
#         return AuthUserCart.objects.get(authuser=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super(CartView, self).get_context_data(**kwargs)
#         context['FEATURE_NAME_BUYANDTRY'] = settings.FEATURE_NAME_BUYANDTRY
#         context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

#         # TODO: do not add 'site_name' to context
#         # once the 'sites' are setup in settings
#         context['site_name'] = settings.SITE_NAME
#         return context


# class CartCheckoutCallbackView(LoginRequiredMixin, generic.DetailView):
#     template_name = 'members/purchase/cart.html'
#     context_object_name = 'cart'
#     model = AuthUserCart

#     def get_object(self, queryset=None):
#         return AuthUserCart.objects.get(authuser=self.request.user)

#     def post(self, request, *args, **kwargs):
#         try:
#             # create new order
#             order = AuthUserOrder()
#             order.authuser = self.request.user
#             order.save()
#             logger.debug('Created new order %d' % order.id)

#             cart = self.get_object()

#             order_type = request.POST['order_type'].strip().lower()
#             capture_order = (order_type == 'buy')

#             # create charge with stripe,
#             try:
#                 token_id = request.POST['token[id]']
#                 total_amount_in_cents = int(request.POST['total_amount'])

#                 if(total_amount_in_cents != cart.get_cart_total_in_cents()):
#                     # either cart has changed since payment or
#                     # user is trying something nasty
#                     # in any case we have a discrepancy between
#                     # what was shown to the user at the time of checkout
#                     # and current cart contents
#                     # it is best to stop right here and refresh the cart
#                     # so that user can checkout again
#                     logger.info('Cart total did not match the total that came in the request')
#                     return JsonResponse({'status': 'error', 'message': 'Total ammount does not match.'})

#                 order_type = request.POST['order_type']
#                 stripe.api_key = settings.STRIPE_SECRET_KEY
#                 stripe.Charge.create(
#                                     amount=total_amount_in_cents,
#                                     currency="usd",
#                                     card=token_id,
#                                     capture=capture_order,
#                                     metadata={
#                                             'order_id': order.id,
#                                             'order_type': order_type
#                                             })

#             except Exception, e:
#                 logger.error('Error in CartCheckoutCallbackView.post()')
#                 logger.error(str(e))
#                 return JsonResponse({'status': 'error', 'message': 'Failed to charge credit card.'})

#             # create or update shipping address
#             #
#             # TODO: allow multiple addresses per user
#             # right now there is only one address per user which
#             # is enforced in the database with a Unique key on user id
#             shipping_address = None
#             try:
#                 shipping_address = AuthUserAddress.objects.get(authuser=self.request.user)
#                 logger.debug('Updating existing shipping address')
#             except AuthUserAddress.DoesNotExist:
#                 # no address, that's ok we will create a new one
#                 shipping_address = AuthUserAddress()
#                 logger.debug('Creating new shipping address')

#             # TODO: shipping address should be tied to the order
#             # right not it is only tied to user
#             shipping_address.authuser = self.request.user
#             shipping_address.street = request.POST['args[shipping_address_line1]']
#             shipping_address.city = request.POST['args[shipping_address_city]']
#             shipping_address.state = request.POST['args[shipping_address_state]']
#             shipping_address.zipcd = request.POST['args[shipping_address_zip]']
#             shipping_address.shipping = True
#             shipping_address.save()

#             # add items to order
#             for product in cart.saved_items.all():
#                 order_item = AuthUserOrderItem()
#                 order_item.product = product
#                 order_item.order = order
#                 order_item.sell_price = product.current_price
#                 order_item.captured = capture_order
#                 if(capture_order):
#                     order_item.capture_time = timezone.now()
#                 else:
#                     order_item.capture_time = timezone.now() + timedelta(hours=settings.STRIPE_CAPTURE_TRANSACTION_TIME)
#                 order_item.quantity = 1
#                 order_item.save()
#             logger.debug('Added items to order')

#             # all items have been saved in the order now remove them from the cart
#             # TODO: once the item is purchased the total available quantity should be adjusted
#             # which we don't keep track of right now anywhere
#             for product in cart.saved_items.all():
#                 cart.saved_items.remove(product)
#                 logger.debug('removing from cart %s' % str(order_item.product))
#             cart.save()
#             logger.debug('Removed items from cart')

#             return JsonResponse({'status': 'ok', 'message': 'Order is completed.'})
#         except Exception, e:
#             logger.error('Error in CartCheckoutCallbackView.post()')
#             logger.error(str(e))
#             return JsonResponse({'status': 'error', 'message': 'Error processing the order.'})
