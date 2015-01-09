from django.shortcuts import render
from django.http import JsonResponse 
from django.views import generic
from members.models import AuthUserActivity, AuthUser
from goods.models import Product
from members.forms import CustomAuthenticationForm
from django.contrib.auth import views
from django.views.decorators.csrf import csrf_exempt


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

# @csrf_exempt
def ProductLike(request):

	if request.method == "POST":
		print(request.POST['id'])
		userinstance = request.user
		product = Product.objects.get(pk=int(request.POST['id'][6:]))
		useractivity = AuthUserActivity.objects.get(authuser=userinstance)
		if product in useractivity.saved_items.all():
			useractivity.saved_items.remove(product)
		else:
			useractivity.saved_items.add(product)
		useractivity.save()
		return JsonResponse('success', safe=False)
	else:
		return JsonResponse('success', safe=False)


