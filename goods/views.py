from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from goods.models import Product
from merchants.models import Store

class HomeView(generic.ListView):
	template_name = 'goods/home/home.html'
	context_object_name = 'goods'
	model = Product

class DetailView(generic.DetailView):
	template_name = 'goods/detail/detail.html'
	context_object_name = 'product'
	model = Product

class MapView(generic.ListView):
	template_name = 'goods/map/map.html'
	context_object_name = 'stores'
	model = Store