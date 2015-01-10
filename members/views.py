from django.http import JsonResponse 
from django.views import generic
from members.models import AuthUserActivity, AuthUser, AuthUserCart
from goods.models import Product
from members.forms import CustomAuthenticationForm
from braces.views import LoginRequiredMixin	
from django.contrib.auth.decorators import login_required

class ClosetView(generic.ListView):
	template_name = 'members/closet/closet.html'
	context_object_name = 'saved_items'
	model = AuthUserActivity


# #Needs to be updated implemented with registration/signup modal
# class SignupView(generic.FormView):
# 	template_name = 'members/auth/signup.html'
# 	model = AuthUser
# 	form_class = CustomAuthenticationForm

# 	def post(self, request, *args, **kwargs):
# 	    form_class = self.get_form_class()
# 	    form = self.get_form(form_class)
# 	    if form.is_valid():
# 	        return self.form_valid(form)
# 	    else:
# 	        return self.form_invalid(form)

@login_required
def ProductLike(request):
	"""Adds product instance to 'saved_items' field of 
		AuthUserActivity model
	"""
	#
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
		return JsonResponse(product.id, safe=False)
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
		return context

class CheckoutView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'members/purchase/checkout.html'

class ReviewView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'members/purchase/review.html'

class PaymentView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'members/purchase/payment.html'
