from django.views import generic
from goods.models import Product, Category, FurnitureType, Segment, ProductImage, Color, Style
from members.models import AuthUserActivity, OfferType, PromotionOffer
from django.core.serializers import serialize
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
# from goods.forms import CommentForm
from random import randint
import logging
from django.conf import settings
from random import shuffle
from helper import Neighborhoods

from endless_pagination.views import AjaxListView



logger = logging.getLogger(__name__)

BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'


class LandingView(generic.ListView):
    template_name = 'goods/landing/landing.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        queryset = self.model.objects.filter(is_landing=True, store__is_featured=True)[:9]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        #JSON sent to client to calc distance from user
        # context['products_json'] = serialize('json', context['products'])
        context['BaseUrl'] = BASE_URL
        context['FEATURE_NAME_RESERVE'] = settings.FEATURE_NAME_RESERVE
        context['FEATURE_TOOLTIP_RESERVE'] = settings.FEATURE_TOOLTIP_RESERVE
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['SIGNUP_OFFER'] = settings.SIGNUP_OFFER
        
        
        # TODO: do not add 'site_name' to context
        # once the 'sites' are setup in settings
        context['site_name'] = settings.SITE_NAME
        # removed until profile page implemented
        # context['liked_items'] = get_liked_items(self.request.user)

        # add any "First time" offers
        # if there is more than one get the first one
        print (self.request.session.items())
        if(not self.request.session.get('seen_offers', False)):
            offers = PromotionOffer.get_current_offers(user=self.request.user, offer_type=OfferType.FIRST_ORDER)
            if(offers):
                context['promotion_offer'] = offers[0]

                # seen_offers flag in session will tell us next time
                # whether we should show this offer or not
                # expiration is needed so that after this flag expires
                # we will show the offer again
                self.request.session['seen_offers'] = True
                self.request.session.set_expiry(settings.OFFER_MODAL_EXPIRATION)

        return context

class MainView(AjaxListView):
    template_name = 'goods/main/main_ajax.html'
    page_template = 'goods/main/main_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'
    

    def get_queryset(self):
        try:
            furn_type = self.request.GET['type']
            try:
                furniture_type_object = FurnitureType.objects.get(select=furn_type)
            except Exception, e:
                logger.debug(str(e))
                furniture_type_object = None
            queryset = list(self.model.objects.filter(is_published=True, furnituretype = furniture_type_object, store__is_featured=True))
        except:
            queryset = self.model.objects.filter(is_published=True, store__is_featured=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['FEATURE_NAME_RESERVE'] = settings.FEATURE_NAME_RESERVE
        context['FEATURE_TOOLTIP_RESERVE'] = settings.FEATURE_TOOLTIP_RESERVE
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['query_operator'] = '&'
        context['searchfilter'] = {
                                   'price_slider_min': 0,
                                   'price_slider_max': 10000,
                                   'height_slider_min': 0,
                                   'height_slider_max': 1000,
                                   'width_slider_min': 0,
                                   'width_slider_max': 1000,
                                   'depth_slider_min': 0,
                                   'depth_slider_max': 1000,
                                   'segments': Segment.objects.all(),
                                   'colors': Color.objects.all(),
                                   'styles': Style.objects.all(),
                                   'furnituretypes': FurnitureType.objects.all(),
                                   'neighborhoods': Neighborhoods['SF']
                                   }
        
        # TODO: do not add 'site_name' to context
        # once the 'sites' are setup in settings
        context['site_name'] = settings.SITE_NAME
        # removed until profile page implemented
        # context['liked_items'] = get_liked_items(self.request.user)
        return context


class SearchFilterView(AjaxListView):
    template_name = 'goods/main/main_ajax_page.html'
    page_template = 'goods/main/main_ajax_page.html'

    context_object_name = 'products'
    model = Product
    key = 'page'

    def get_queryset(self):

        queryset = self.model.objects.filter(is_published=True)
        segments = [int(i) for i in self.request.GET.getlist('filter-segment')]
        if(segments):
            queryset = queryset.filter(segment__in=segments)

        colors = [int(i) for i in self.request.GET.getlist('filter-color')]
        if(colors):
            queryset = queryset.filter(color__in=colors)

        # TODO: enable styles, styles are for now disabled
        # styles = [int(i) for i in self.request.GET.getlist('filter-style')]
        # if(styles):
        #    queryset = queryset.filter(style__in=styles)

        furnituretypes = [int(i) for i in self.request.GET.getlist('filter-furnituretype')]
        if(furnituretypes):
            queryset = queryset.filter(furnituretype__in=furnituretypes)

        neighborhoods = self.request.GET.getlist('filter-neighborhood')
        if(neighborhoods):
            queryset = queryset.filter(store__neighborhood__in=neighborhoods)

        price_min = self.request.GET.get('filter-price-min', None)
        if(price_min):
            price_min = int(price_min)
            queryset = queryset.filter(current_price__gte=price_min)

        price_max = self.request.GET.get('filter-price-max', None)
        if(price_max):
            price_max = int(price_max)
            queryset = queryset.filter(current_price__lte=price_max)

        height_min = self.request.GET.get('filter-height-min', None)
        if(height_min):
            height_min = int(height_min)
            queryset = queryset.filter(height__gte=height_min)

        height_max = self.request.GET.get('filter-height-max', None)
        if(height_max):
            height_max = int(height_max)
            queryset = queryset.filter(height__lte=height_max)

        width_min = self.request.GET.get('filter-width-min', None)
        if(width_min):
            width_min = int(width_min)
            queryset = queryset.filter(width__gte=width_min)

        width_max = self.request.GET.get('filter-width-max', None)
        if(width_max):
            width_max = int(width_max)
            queryset = queryset.filter(width__lte=width_max)

        depth_min = self.request.GET.get('filter-depth-min', None)
        if(depth_min):
            depth_min = int(depth_min)
            queryset = queryset.filter(depth__gte=depth_min)

        depth_max = self.request.GET.get('filter-depth-max', None)
        if(depth_max):
            depth_max = int(depth_max)
            queryset = queryset.filter(depth__lte=depth_max)

        return queryset


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


# class DirectionsView(LoginRequiredMixin, generic.DetailView):
#     template_name = 'goods/detail/map.html'
#     context_object_name = 'product'
#     model = Product

#     def get_context_data(self, **kwargs):
#         context = super(DirectionsView, self).get_context_data(**kwargs)
#         context['store'] = self.object.store
#         return context


# Gets list of liked items to populate 'active' hearts
def get_liked_items(user):
    """ Creates list of user's liked items for json
    Obj passed to addlikehearts js script
    """
    if(not user.is_authenticated()):
        return []

    useractivity, new = AuthUserActivity.objects.get_or_create(authuser=user)
    if new:
        useractivity.save()
    liked_list = useractivity.saved_items.all()
    liked_ids = [prod.id for prod in liked_list]
    return liked_ids

#####Additional views for copy pages######

# class ContactView(generic.TemplateView):
#     template_name = 'goods/copy/contact.html'


# class BlogView(generic.TemplateView):
#     template_name = 'goods/copy/blog.html'


# class BlogPostView(generic.TemplateView):
#     template_name = 'goods/copy/blogpost.html'
