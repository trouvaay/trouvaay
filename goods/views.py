from django.views import generic
from goods.models import Product, Category, Segment
from members.models import AuthUserActivity
from django.core.serializers import serialize
from braces.views import LoginRequiredMixin
from goods.forms import CommentForm
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
		""" Show most recent six unsold items"""
		queryset = self.model.objects.filter(is_published=True, is_sold=False)[:6]
		return queryset

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['products_json'] = serialize('json', context['pieces'])
		try:
			context['sold_pieces'] = self.model.objects.filter(is_published=True, is_sold=True)[0]
		except:
			pass
		try:
			context['featured_pieces'] = self.model.objects.filter(is_published=True, is_featured=True)[0]
		except:
			pass
		return context


class NewView(LoginRequiredMixin, generic.ListView):
	template_name = 'goods/new/new.html'
	context_object_name = 'goods'
	model = Product
	new = Segment.objects.filter(select='new')[0]
	#need to find out how to ref request.user when not a post request and /
	#then update json of liked ids passed to template

	def get_queryset(self):
		
		queryset = self.model.objects.filter(is_published=True,segment=self.new)
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


class DirectionsView(LoginRequiredMixin, generic.DetailView):
	template_name = 'goods/home/map.html'
	context_object_name = 'product'
	model = Product

	def get_context_data(self, **kwargs):
		context = super(DirectionsView, self).get_context_data(**kwargs)
		context['store'] = self.object.store
		# context['store_json'] = serialize('json', [self.object.store])
		return context


class AboutView(generic.TemplateView):
	template_name = 'goods/copy/about.html'


class ContactView(generic.TemplateView):
	template_name = 'goods/copy/contact.html'


class BlogView(generic.TemplateView):
	template_name = 'goods/copy/blog.html'


class BlogPostView(generic.TemplateView):
	template_name = 'goods/copy/blogpost.html'