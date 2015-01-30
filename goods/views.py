from django.views import generic
from goods.models import Product, Category, FurnitureType, Segment, ProductImage
from members.models import AuthUserActivity
from django.core.serializers import serialize
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
# from goods.forms import CommentForm
from random import randint
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'


class HomeView(generic.ListView):
    template_name = 'goods/home/home.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 30

    def get_queryset(self):
        pub_products = self.model.objects.filter(is_published=True)
        #filter by products that are furniture
        queryset = [i for i in pub_products if i.is_furniture()]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        #JSON sent to client to calc distance from user
        # context['products_json'] = serialize('json', context['products'])
        context['BaseUrl'] = BASE_URL
        context['FEATURE_NAME_RESERVE'] = settings.FEATURE_NAME_RESERVE
        context['FEATURE_TOOLTIP_RESERVE'] = settings.FEATURE_TOOLTIP_RESERVE
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        
        # TODO: do not add 'site_name' to context
        # once the 'sites' are setup in settings
        context['site_name'] = settings.SITE_NAME
        # removed until profile page implemented
        # context['liked_items'] = get_liked_items(self.request.user)
        return context

class FurnitureTypeView(generic.ListView):
    template_name = 'goods/home/furniture_type.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 30
    

    def get_queryset(self):
        furn_type = self.request.GET['type']
        try:
            furniture_type_object = FurnitureType.objects.get(select=furn_type)
        except Exception, e:
            logger.debug(str(e))
            furniture_type_object = None
        queryset = self.model.objects.filter(is_published=True,furnituretype = furniture_type_object )
        #filter by products that are furniture
        return queryset

    def get_context_data(self, **kwargs):
        context = super(FurnitureTypeView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['FEATURE_NAME_RESERVE'] = settings.FEATURE_NAME_RESERVE
        context['FEATURE_TOOLTIP_RESERVE'] = settings.FEATURE_TOOLTIP_RESERVE
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        
        # TODO: do not add 'site_name' to context
        # once the 'sites' are setup in settings
        context['site_name'] = settings.SITE_NAME
        # removed until profile page implemented
        # context['liked_items'] = get_liked_items(self.request.user)
        return context


class VintageView(generic.ListView):
    # TODO: update view to reflect instagrammy feed.  Will mimic DetailView
    template_name = 'goods/vintage/vintage.html'
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


class DetailView(generic.DetailView):
    template_name = 'goods/detail/detail.html'
    context_object_name = 'product'
    model = Product
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # removed until profile page implemented
        # context['liked_items'] = get_liked_items(self.request.user)
        context['returns'] = settings.RETURN_POLICY
        context['FEATURE_NAME_RESERVE'] = settings.FEATURE_NAME_RESERVE
        context['FEATURE_TOOLTIP_RESERVE'] = settings.FEATURE_TOOLTIP_RESERVE
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY     
        return context


class AboutView(generic.TemplateView):
    template_name = 'goods/copy/about.html'


class DirectionsView(LoginRequiredMixin, generic.DetailView):
    template_name = 'goods/detail/map.html'
    context_object_name = 'product'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(DirectionsView, self).get_context_data(**kwargs)
        context['store'] = self.object.store
        return context


# Gets list of liked items to populate 'active' hearts
# def get_liked_items(user):
#     """ Creates list of user's liked items for json
#     Obj passed to addlikehearts js script
#     """
#     if(not user.is_authenticated()):
#         return []

#     useractivity, new = AuthUserActivity.objects.get_or_create(authuser=user)
#     if new:
#         useractivity.save()
#     liked_list = useractivity.saved_items.all()
#     liked_ids = [prod.id for prod in liked_list]
#     return liked_ids

#####Additional views for copy pages######

# class ContactView(generic.TemplateView):
#     template_name = 'goods/copy/contact.html'


# class BlogView(generic.TemplateView):
#     template_name = 'goods/copy/blog.html'


# class BlogPostView(generic.TemplateView):
#     template_name = 'goods/copy/blogpost.html'
