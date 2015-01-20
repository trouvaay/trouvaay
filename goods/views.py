from django.views import generic
from goods.models import Product, Category, FurnitureType, Segment, ProductImage
from members.models import AuthUserActivity
from django.core.serializers import serialize
from braces.views import LoginRequiredMixin
# from goods.forms import CommentForm
from random import randint
from django.conf import settings


BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'


def get_liked_items(user):
	""" Creates list of user's liked items for json
	Obj passed to addlikehearts js script
	"""

	useractivity, new = AuthUserActivity.objects.get_or_create(authuser=user)
	if new:
		useractivity.save()
	liked_list = useractivity.saved_items.all()
	liked_ids = [prod.id for prod in liked_list]
	return liked_ids


class HomeView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'goods/home/home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context_product = Product.objects.get(short_name='HomepgFeatured')
		context_imgs = ProductImage.objects.filter(product=context_product).all()
		context['vintage'] = context_imgs[0]
		context['new'] = context_imgs[1]
		return context


class NewView(LoginRequiredMixin, generic.ListView):
	template_name = 'goods/new/new.html'
	context_object_name = 'products'
	model = Product
	try:
		new = Segment.objects.filter(select='new')[0]
	except:
		new = None

	def get_queryset(self):
		queryset = self.model.objects.filter(is_published=True,segment=self.new).exclude(description="")
		return queryset

	def get_context_data(self, **kwargs):
		context = super(NewView, self).get_context_data(**kwargs)
		#JSON sent to client to calc distance from user
		context['products_json'] = serialize('json', context['products'])
		for furnituretype in FurnitureType.objects.all():
			context[(str(furnituretype))] = self.model.objects.filter(furnituretype=furnituretype, is_published=True, segment=self.new).exclude(description="")
		context['BaseUrl'] = BASE_URL
		context['liked_items'] = get_liked_items(self.request.user)
		return context


class VintageView(LoginRequiredMixin, generic.ListView):
	# TODO: update view to reflect instagrammy feed.  Will mimic DetailView
	template_name = 'goods/vintage/vintage2.html'
	context_object_name = 'products'
	model = Product
	vintage = Segment.objects.filter(select='vintage')[0]

	def get_queryset(self):
		
		queryset = self.model.objects.filter(is_published=True,segment=self.vintage)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(VintageView, self).get_context_data(**kwargs)
		context['products_json'] = serialize('json', context['products'])
		for furnituretype in FurnitureType.objects.all():
			context[(str(furnituretype))] = self.model.objects.filter(furnituretype=furnituretype, is_published=True, segment=self.vintage)
		context['BaseUrl'] = BASE_URL
		context['liked_items'] = get_liked_items(self.request.user)
		return context


class DetailView(LoginRequiredMixin, generic.DetailView):
	template_name = 'goods/detail/detail.html'
	context_object_name = 'product'
	model = Product

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		context['liked_items'] = get_liked_items(self.request.user)
		context['returns'] = settings.RETURN_POLICY
		return context


class DirectionsView(LoginRequiredMixin, generic.DetailView):
	template_name = 'goods/detail/map.html'
	context_object_name = 'product'
	model = Product

	def get_context_data(self, **kwargs):
		context = super(DirectionsView, self).get_context_data(**kwargs)
		context['store'] = self.object.store
		return context


class AboutView(generic.TemplateView):
	template_name = 'goods/copy/about.html'


class ContactView(generic.TemplateView):
	template_name = 'goods/copy/contact.html'


class BlogView(generic.TemplateView):
	template_name = 'goods/copy/blog.html'


class BlogPostView(generic.TemplateView):
	template_name = 'goods/copy/blogpost.html'