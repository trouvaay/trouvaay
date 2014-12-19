from django.shortcuts import render
from django.views import generic
from members.models import AuthUserActivity
from members.forms import CustomAuthenticationForm
from django.contrib.auth import views

class ClosetView(generic.ListView):
	template_name = 'members/closet/closet.html'
	context_object_name = 'saved_items'
	model = AuthUserActivity

# def login(request):
# 	if request.method == 'POST':
# 		form = CustomAuthenticationForm(request, data=request.POST)
# 		print (form)
# 		if form.is_valid():
# 			print('it worked!')
# 		else:
# 			print ('it didnt work')
# 			print (form.errors)
# 	else:
# 		print ('wasnt a post method!')
# 		form = CustomAuthenticationForm()
	
# 	return render(request, 'members/auth/login.html', {'form':form})

# class login 