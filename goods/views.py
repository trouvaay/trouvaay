from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from goods.models import Product
from merchants.models import Store
from django.core.serializers import serialize

class HomeView(generic.ListView):
	template_name = 'goods/home/home.html'
	context_object_name = 'goods'
	model = Product

class DetailView(generic.DetailView):
	template_name = 'goods/detail/detail.html'
	context_object_name = 'product'
	model = Product

class MapView(generic.DetailView):
	template_name = 'goods/map/map.html'
	context_object_name = 'product'
	model = Product

	def get_context_data(self, **kwargs):
		context = super(MapView, self).get_context_data(**kwargs)
		context['store'] = self.object.store
		context['store_json'] = serialize('json', [self.object.store])
		print (context['store_json'])
		return context