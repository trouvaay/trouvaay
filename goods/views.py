from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from goods.models import Product

class HomeView(generic.ListView):
	template_name = 'goods/home.html'
	context_object_name = 'goods'
	model = Product