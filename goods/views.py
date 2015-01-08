from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from goods.models import Product, Category, Segment
from members.models import AuthUserActivity
from merchants.models import Store
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from braces.views import LoginRequiredMixin
from goods.forms import CommentForm
from django.views.generic.detail import SingleObjectMixin
from pprint import pprint as pp
from random import randint

BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'

class HomeView(LoginRequiredMixin, generic.ListView):
	template_name = 'goods/home/home.html'
	context_object_name = 'pieces'
	model = Product

	# Temporary 'curation' of nearby products.  currently just taking first 4 items
	#will eventually need to update to reflect likes of user
	UserCatPref = Category.objects.all()[randint(0,Category.objects.count()-1)]

	def get_queryset(self):
		
		queryset = self.model.objects.filter(is_published=True, is_sold=False)[:3]
		return queryset

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		# print (context['products'])
		context['products_json'] = serialize('json', context['pieces'])
		try:
			context['sold_pieces'] = self.model.objects.filter(is_published=True, is_sold=True)[0]
		except:
			pass
		try:
			context['featured_pieces'] = self.model.objects.filter(is_published=True, is_featured=True)[0]
		except:
			pass
		print(self.request.session.items())
		return context

class NewView(LoginRequiredMixin, generic.ListView):
	template_name = 'goods/new/new.html'
	context_object_name = 'goods'
	model = Product
	new = Segment.objects.filter(select='new')[0]
	#need to find out how to ref request.user when not a post request and /
	#then update json of liked ids passed to template
	

	def get_queryset(self):
		
		queryset = self.model.objects.filter(is_published=True,segment=self.new)[:10]
		return queryset

	def get_context_data(self, **kwargs):
		context = super(NewView, self).get_context_data(**kwargs)
		# context['products_json'] = serialize('json', context['goods'])
		for room in Category.objects.all():
			context[(str(room))] = self.model.objects.filter(category=room, is_published=True, segment=self.new)
		# context['image'] = context['goods'].order_by('-id')[0].productimage_set.first()
		# rest.dist = getDist(fromLat=session.lat,fromLng=session.lng,toLat=rest.lat,toLng=rest.lng)		
		context['BaseUrl'] = BASE_URL	
		useractivity = AuthUserActivity.objects.get(authuser=self.request.user)
		liked_list = useractivity.saved_items.filter(segment=self.new).all()
		liked_ids = [prod.id for prod in liked_list]
		print(liked_ids)
		context['liked_items'] = liked_ids
		return context

class VintageView(LoginRequiredMixin, generic.ListView):
	template_name = 'goods/new/new.html'
	context_object_name = 'goods'
	model = Product
	vintage = Segment.objects.filter(select='vintage')[0]
	# rest.dist = getDist(fromLat=session.lat,fromLng=session.lng,toLat=rest.lat,toLng=rest.lng)

	def get_queryset(self):
		
		queryset = self.model.objects.filter(is_published=True,segment=self.vintage)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(VintageView, self).get_context_data(**kwargs)
		# context['products_json'] = serialize('json', context['goods'])
		for room in Category.objects.all():
			context[(str(room))] = self.model.objects.filter(category=room, is_published=True, segment=self.vintage)
		# context['image'] = context['goods'].order_by('-id')[0].productimage_set.first()
		context['BaseUrl'] = BASE_URL
		return context

class DetailView(generic.DetailView):
	template_name = 'goods/detail/detail.html'
	context_object_name = 'product'
	model = Product
	
	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		context['comments'] = self.object.comment_set.all()
		context['form'] = CommentForm()
		return context

class DetailCommentView(SingleObjectMixin, SuccessMessageMixin, generic.FormView):
	template_name = 'goods/detail/detail.html'
	form_class = CommentForm
	model = Product
	success_message = "comment was posted"

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseForbidden()
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		form.helper.form_action = reverse('goods:detail', args=[self.object.pk])
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)
		
		

	def form_valid(self, form):
		model_instance = form.save(commit=False)
		model_instance.authuser = self.request.user
		model_instance.product = self.object
		model_instance.save()
		# form.cleaned_data
		return super(DetailCommentView, self).form_valid(form)

	def get_success_url(self):
		return reverse('goods:detail', kwargs={'pk': self.object.pk})


class DetailRouteView(LoginRequiredMixin, generic.View):

	def get(self, request, *args, **kwargs):
		view = DetailView.as_view()
		return view(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		view = DetailCommentView.as_view()
		return view(request, *args, **kwargs)


class MapView(LoginRequiredMixin, generic.DetailView):
	template_name = 'goods/home/map.html'
	context_object_name = 'product'
	model = Product

	def get_context_data(self, **kwargs):
		context = super(MapView, self).get_context_data(**kwargs)
		context['store'] = self.object.store
		# context['store_json'] = serialize('json', [self.object.store])
		return context

class StoreView(LoginRequiredMixin, generic.DetailView):
	template_name = 'goods/merchants/storeprofile.html'
	context_object_name = 'store'
	model = Store

	def get_context_data(self, **kwargs):
		context = super(StoreView, self).get_context_data(**kwargs)
		context['products'] = self.object.product_set.all()
		context['retailer'] = self.object.retailer
		return context