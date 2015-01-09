from django.shortcuts import render
from django.http import JsonResponse 
from django.views import generic
from members.models import AuthUserActivity, AuthUser, AuthUserCart
from goods.models import Product
from members.forms import CustomAuthenticationForm
from django.contrib.auth import views
from braces.views import LoginRequiredMixin	

class ClosetView(generic.ListView):
	template_name = 'members/closet/closet.html'
	context_object_name = 'saved_items'
	model = AuthUserActivity

class SignupView(generic.FormView):
	template_name = 'members/auth/signup.html'
	model = AuthUser
	form_class = CustomAuthenticationForm

	def post(self, request, *args, **kwargs):
	    form_class = self.get_form_class()
	    form = self.get_form(form_class)
	    if form.is_valid():
	        return self.form_valid(form)
	    else:
	        return self.form_invalid(form)

class SignupView(generic.CreateView):
	template_name = 'members/auth/signup.html'
	model = AuthUser
	form_class = CustomAuthenticationForm

def ProductLike(request):

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
	template_name = 'members/cart/cart.html'
	context_object_name = 'cart'
	model = AuthUserCart

	def get_object(self, queryset=None):
		return AuthUserCart.objects.get(authuser=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(CartView, self).get_context_data(**kwargs)
		return context
