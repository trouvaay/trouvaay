from django.views import generic
from goods.models import Product, Category, FurnitureType, Segment, ProductImage, Color, Style, Subcategory
from members.models import AuthUserActivity, OfferType, PromotionOffer
from django.core.serializers import serialize
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
# from goods.forms import CommentForm
from random import randint
import logging
from django.conf import settings
from random import shuffle

from helper import is_time_to_show_modal, hide_modal, Neighborhoods
import uuid

# from helper import get_liked_items

from pprint import pprint as pp
from endless_pagination.views import AjaxListView



logger = logging.getLogger(__name__)

BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'

price_slider_max = 2000


# <<<<<<< HEAD
# class LandingView(generic.ListView):
#     template_name = 'goods/landing/landing.html'
#     context_object_name = 'products'
#     model = Product

#     def get_queryset(self):
#         queryset = self.model.objects.filter(is_landing=True, store__is_featured=True)[:6]
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(LandingView, self).get_context_data(**kwargs)

#         if(not self.request.session.get('cid', None)):
#             self.request.session['cid'] = str(uuid.uuid4())

#         context['BaseUrl'] = BASE_URL
#         if(settings.ENABLE_REFERRAL):
#             if(self.request.user.is_authenticated()):
#                 if(is_time_to_show_modal(self.request, 'referral2')):
#                     logger.info('we should be showing 2nd modal')
#                     context['show_referral_second_modal'] = True
#                     hide_modal(self.request, 'referral2', settings.SECOND_REFERRAL_MODAL_EXP)
#             else:
#                 if(is_time_to_show_modal(self.request, 'referral1')):
#                     logger.info('we should be showing 1st modal')
#                     context['show_referral_first_modal'] = True
#                     hide_modal(self.request, 'referral1', settings.FIRST_REFERRAL_MODAL_EXP)


#         context['SIGNUP_OFFER'] = settings.SIGNUP_OFFER

#         # add any "First time" offers
#         #only FIRST_ORDERs. DISCOUNT_PROMOs arent rendered
#         # if there is more than one get the first one
#         print('show_modal: ', is_time_to_show_modal(self.request, 'offer_modal'))
#         if(is_time_to_show_modal(self.request, 'offer_modal')):
# #         if(not self.request.session.get('seen_offers', False)):
#             offers = PromotionOffer.get_current_offers(user=self.request.user, offer_type=OfferType.FIRST_ORDER)
#             print('offers:', offers)
#             if(offers):
#                 context['promotion_offer'] = offers[0]

#                 # seen_offers flag in session will tell us next time
#                 # whether we should show this offer or not
#                 # expiration is needed so that after this flag expires
#                 # we will show the offer again
#                 hide_modal(self.request, 'offer_modal', settings.OFFER_MODAL_EXPIRATION)
# #                 self.request.session['seen_offers'] = True
# #                 self.request.session.set_expiry(settings.OFFER_MODAL_EXPIRATION)

#         return context

class LandingView(AjaxListView):
    template_name = 'goods/main/hunt_ajax.html'
    page_template = 'goods/main/hunt_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'


    # def get_queryset(self):
    #     try:
    #         furn_type = self.request.GET['type']
    #         try:
    #             furniture_type_object = FurnitureType.objects.get(select=furn_type)
    #         except Exception, e:
    #             logger.debug(str(e))
    #             furniture_type_object = None
    #         queryset = list(self.model.objects.filter(is_published=True, furnituretype = furniture_type_object, store__is_featured=True))
    #     except:
    #         queryset = self.model.objects.filter(is_published=True, store__is_featured=True)

    #     return queryset
    def get_queryset(self):
        queryset = self.model.objects.filter(is_published=True, the_hunt=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['searchfilter'] = {
                                   'price_slider_min': 0,
                                   'price_slider_max': price_slider_max,
                                   'height_slider_min': 0,
                                   'height_slider_max': 72,
                                   'width_slider_min': 0,
                                   'width_slider_max': 120,
                                   'depth_slider_min': 0,
                                   'depth_slider_max': 72,
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
        if(not self.request.session.get('cid', None)):
            self.request.session['cid'] = str(uuid.uuid4())

        # if(settings.ENABLE_REFERRAL):
        #     if(self.request.user.is_authenticated()):
        #         if(is_time_to_show_modal(self.request, 'referral2')):
        #             logger.info('we should be showing 2nd modal')
        #             context['show_referral_second_modal'] = True
        #             hide_modal(self.request, 'referral2', settings.SECOND_REFERRAL_MODAL_EXP)
        #     else:
        #         if(is_time_to_show_modal(self.request, 'referral1')):
        #             logger.info('we should be showing 1st modal')
        #             context['show_referral_first_modal'] = True
        #             hide_modal(self.request, 'referral1', settings.FIRST_REFERRAL_MODAL_EXP)


        context['SIGNUP_OFFER'] = settings.SIGNUP_OFFER
        # add any "First time" offers
        #only FIRST_ORDERs. DISCOUNT_PROMOs arent rendered
        # if there is more than one get the first one

#         if(is_time_to_show_modal(self.request, 'offer_modal')):
# #         if(not self.request.session.get('seen_offers', False)):
#             offers = PromotionOffer.get_current_offers(user=self.request.user, offer_type=OfferType.FIRST_ORDER)
#             print('offers:', offers)
#             if(offers):
#                 context['promotion_offer'] = offers[0]

#                 # seen_offers flag in session will tell us next time
#                 # whether we should show this offer or not
#                 # expiration is needed so that after this flag expires
#                 # we will show the offer again
#                 hide_modal(self.request, 'offer_modal', settings.OFFER_MODAL_EXPIRATION)
#                 self.request.session['seen_offers'] = True
#                 self.request.session.set_expiry(settings.OFFER_MODAL_EXPIRATION)

        if(is_time_to_show_modal(self.request, 'login_modal')):
            logger.info('we should be showing login modal')
            context['show_login_modal'] = True
            hide_modal(self.request, 'login_modal', settings.LOGIN_MODAL_EXP)

        return context


class ShopView(AjaxListView):
    template_name = 'goods/main/shop_ajax.html'
    page_template = 'goods/main/landing_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'


    # def get_queryset(self):
    #     try:
    #         furn_type = self.request.GET['type']
    #         try:
    #             furniture_type_object = FurnitureType.objects.get(select=furn_type)
    #         except Exception, e:
    #             logger.debug(str(e))
    #             furniture_type_object = None
    #         queryset = list(self.model.objects.filter(is_published=True, furnituretype = furniture_type_object, store__is_featured=True))
    #     except:
    #         queryset = self.model.objects.filter(is_published=True, store__is_featured=True)

    #     return queryset
    def get_queryset(self):
        queryset = self.model.objects.filter(is_published=True, hours_left__gte=0, store__is_featured=True).exclude(description__isnull=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['searchfilter'] = {
                                   'price_slider_min': 0,
                                   'price_slider_max': price_slider_max,
                                   'height_slider_min': 0,
                                   'height_slider_max': 72,
                                   'width_slider_min': 0,
                                   'width_slider_max': 120,
                                   'depth_slider_min': 0,
                                   'depth_slider_max': 72,
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
        if(not self.request.session.get('cid', None)):
            self.request.session['cid'] = str(uuid.uuid4())

        # if(settings.ENABLE_REFERRAL):
        #     if(self.request.user.is_authenticated()):
        #         if(is_time_to_show_modal(self.request, 'referral2')):
        #             logger.info('we should be showing 2nd modal')
        #             context['show_referral_second_modal'] = True
        #             hide_modal(self.request, 'referral2', settings.SECOND_REFERRAL_MODAL_EXP)
        #     else:
        #         if(is_time_to_show_modal(self.request, 'referral1')):
        #             logger.info('we should be showing 1st modal')
        #             context['show_referral_first_modal'] = True
        #             hide_modal(self.request, 'referral1', settings.FIRST_REFERRAL_MODAL_EXP)


        context['SIGNUP_OFFER'] = settings.SIGNUP_OFFER
        # add any "First time" offers
        #only FIRST_ORDERs. DISCOUNT_PROMOs arent rendered
        # if there is more than one get the first one

#         if(is_time_to_show_modal(self.request, 'offer_modal')):
# #         if(not self.request.session.get('seen_offers', False)):
#             offers = PromotionOffer.get_current_offers(user=self.request.user, offer_type=OfferType.FIRST_ORDER)
#             print('offers:', offers)
#             if(offers):
#                 context['promotion_offer'] = offers[0]

#                 # seen_offers flag in session will tell us next time
#                 # whether we should show this offer or not
#                 # expiration is needed so that after this flag expires
#                 # we will show the offer again
#                 hide_modal(self.request, 'offer_modal', settings.OFFER_MODAL_EXPIRATION)
#                 self.request.session['seen_offers'] = True
#                 self.request.session.set_expiry(settings.OFFER_MODAL_EXPIRATION)

        if(is_time_to_show_modal(self.request, 'login_modal')):
            logger.info('we should be showing login modal')
            context['show_login_modal'] = True
            hide_modal(self.request, 'login_modal', settings.LOGIN_MODAL_EXP)

        return context


class SearchFilterView(AjaxListView):
    template_name = 'goods/main/landing_ajax_page.html'
    page_template = 'goods/main/landing_ajax_page.html'

    context_object_name = 'products'
    model = Product
    key = 'page'

    def get_queryset(self):

        queryset = self.model.objects.filter(is_published=True)
        segments = [int(i) for i in self.request.GET.getlist('filter-segment')]
        if(segments):
            queryset = queryset.filter(segment__in=segments)

        subcategories = [int(i) for i in self.request.GET.getlist('filter-subcategory')]
        if(subcategories):
            queryset = queryset.filter(subcategory__in=subcategories)

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

        # Filtering price
        price_filter = self.request.GET.get('filter-price', None)
        if price_filter:
            price_min = price_filter.split(';')[0]
            price_max = price_filter.split(';')[1]
        else:
            price_min = self.request.GET.get('filter-price-min', None)
            price_max = self.request.GET.get('filter-price-max', None)

        if(price_min):
            price_min = int(price_min)
            queryset = queryset.filter(current_price__gte=price_min)

        if(price_max):
            price_max = int(price_max)
            if price_max < price_slider_max:
                queryset = queryset.filter(current_price__lte=price_max)


        # Filtering height
        height_filter = self.request.GET.get('filter-height', None)
        if height_filter:
            height_min = height_filter.split(';')[0]
            height_max = height_filter.split(';')[1]
        else:
            height_min = self.request.GET.get('filter-height-min', None)
            height_max = self.request.GET.get('filter-height-max', None)

        if(height_min):
            height_min = int(height_min)
            queryset = queryset.filter(height__gte=height_min)

        if(height_max):
            height_max = int(height_max)
            queryset = queryset.filter(height__lte=height_max)


        # Filtering width
        width_filter = self.request.GET.get('filter-width', None)
        if width_filter:
            width_min = width_filter.split(';')[0]
            width_max = width_filter.split(';')[1]
        else:
            width_min = self.request.GET.get('filter-width-min', None)
            width_max = self.request.GET.get('filter-width-max', None)

        if(width_min):
            width_min = int(width_min)
            queryset = queryset.filter(width__gte=width_min)

        if(width_max):
            width_max = int(width_max)
            queryset = queryset.filter(width__lte=width_max)


        # Filtering depth
        depth_filter = self.request.GET.get('filter-depth', None)
        if depth_filter:
            depth_min = depth_filter.split(';')[0]
            depth_max = depth_filter.split(';')[1]
        else:
            depth_min = self.request.GET.get('filter-depth-min', None)
            depth_max = self.request.GET.get('filter-depth-max', None)

        if(depth_min):
            depth_min = int(depth_min)
            queryset = queryset.filter(depth__gte=depth_min)

        if(depth_max):
            depth_max = int(depth_max)
            queryset = queryset.filter(depth__lte=depth_max)


        return queryset


class DetailView(generic.DetailView):
    template_name = 'goods/detail/detail.html'
    context_object_name = 'product'
    model = Product
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['returns'] = settings.RETURN_POLICY
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['OFFER_IS_ENABLED'] = settings.OFFER_IS_ENABLED

        product = self.get_object()

        # click counter
        exclude_emails = settings.CLICK_EXCLUSIONS
        if(self.request.user.is_authenticated()):
            if not self.request.user.email in exclude_emails:
                product.click_count += 1
                product.save()
                logger.debug('added to click-count')
        else:
            product.click_count += 1
            product.save()
            logger.debug('added to click-count')

        return context


class AboutView(generic.TemplateView):
    template_name = 'goods/copy/about.html'

class ReturnsView(generic.TemplateView):
    template_name = 'goods/copy/returns.html'


# class DirectionsView(LoginRequiredMixin, generic.DetailView):
#     template_name = 'goods/detail/map.html'
#     context_object_name = 'product'
#     model = Product

#     def get_context_data(self, **kwargs):
#         context = super(DirectionsView, self).get_context_data(**kwargs)
#         context['store'] = self.object.store
#         return context


# Gets list of liked items to populate 'active' hearts


#####Additional views for copy pages######

# class ContactView(generic.TemplateView):
#     template_name = 'goods/copy/contact.html'


# class BlogView(generic.TemplateView):
#     template_name = 'goods/copy/blog.html'


# class BlogPostView(generic.TemplateView):
#     template_name = 'goods/copy/blogpost.html'
