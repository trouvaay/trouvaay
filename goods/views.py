import json
from django.views import generic
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from goods.models import Product, Category, FurnitureType, Room, Group, ProductImage, Color, Style, ProductClick
from members.models import AuthUserActivity, OfferType, PromotionOffer
from django.core.serializers import serialize
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
# from goods.forms import CommentForm
from random import randint
import logging
from django.conf import settings
from random import shuffle
from django.utils import timezone

from helper import is_time_to_show_modal, hide_modal, Neighborhoods
import uuid

# from helper import get_liked_items

from pprint import pprint as pp
from endless_pagination.views import AjaxListView



logger = logging.getLogger(__name__)

BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'

price_slider_max = 2000


class ShopView(AjaxListView):
    template_name = 'goods/main/shop_ajax.html'
    page_template = 'goods/main/landing_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'

    def get_queryset(self):
        queryset = self.model.objects.filter(is_published=True, pub_date__lte=timezone.now(), store__is_featured=True).exclude(description__isnull=True)

        rooms = None
        if self.request.GET.get('filter-room'):
            rooms = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]
        if (rooms):
            queryset = queryset.filter(room__in=rooms)

        categories = None
        if self.request.GET.get('filter-category'):
            categories = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        if (categories):
            queryset = queryset.filter(category__in=categories)

        colors = None
        if self.request.GET.get('filter-color'):
            colors = [int(i.strip()) for i in self.request.GET.get('filter-color').split(',')]
        if(colors):
            queryset = queryset.filter(color__in=colors)

        # TODO: enable styles, styles are for now disabled
        # styles = [int(i) for i in self.request.GET.getlist('filter-style')]
        # if(styles):
        #    queryset = queryset.filter(style__in=styles)

        furnituretypes = None
        if self.request.GET.get('filter-furnituretype'):
            furnituretypes = [int(i.strip()) for i in self.request.GET.get('filter-furnituretype').split(',')]
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

    def get_context_data(self, **kwargs):
        print self.request
        context = super(ShopView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

        categories = None
        categories_ids = []
        groups = None
        rooms_ids = []
        groups_ids = []
        if self.request.GET.get('filter-room'):
            rooms_ids = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]

            rooms = Room.objects.filter(pk__in=rooms_ids)
            #context['rooms'] = rooms

            categories = Category.objects.filter(rooms__in=rooms_ids).distinct()
            context['categories'] = categories
        if self.request.GET.get('filter-category'):
            categories_ids = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        #categories_ids = list(set(categories.distinct().values_list('id', flat=True)))
            groups = Group.objects.filter(categories__in=categories_ids).distinct()
            #context['groups'] = groups

        if self.request.GET.get('filter-group'):
            groups_ids = [int(i.strip()) for i in self.request.GET.get('filter-group').split(',')]

        price_filter = self.request.GET.get('filter-price', None)

        if price_filter:
            price_min = price_filter.split(';')[0]
            price_max = price_filter.split(';')[1]
        else:
            price_min = self.request.GET.get('filter-price-min', 0)
            price_max = self.request.GET.get('filter-price-max', 5000)

        # Filtering height
        height_filter = self.request.GET.get('filter-height', None)
        if height_filter:
            height_min = height_filter.split(';')[0]
            height_max = height_filter.split(';')[1]
        else:
            height_min = self.request.GET.get('filter-height-min', 0)
            height_max = self.request.GET.get('filter-height-max', 72)

        # Filtering width
        width_filter = self.request.GET.get('filter-width', None)
        if width_filter:
            width_min = width_filter.split(';')[0]
            width_max = width_filter.split(';')[1]
        else:
            width_min = self.request.GET.get('filter-width-min', 0)
            width_max = self.request.GET.get('filter-width-max', 120)

        # Filtering depth
        depth_filter = self.request.GET.get('filter-depth', None)
        if depth_filter:
            depth_min = depth_filter.split(';')[0]
            depth_max = depth_filter.split(';')[1]
        else:
            depth_min = self.request.GET.get('filter-depth-min', 0)
            depth_max = self.request.GET.get('filter-depth-max', 72)

        context['searchfilter'] = {
                                   'price_slider_min': 0,
                                   'price_slider_max': price_slider_max,
                                   'price_min_val': price_min,
                                   'price_max_val': price_max,
                                   'height_slider_min': 0,
                                   'height_slider_max': 72,
                                   'height_min_val': height_min,
                                   'height_max_val': height_max,
                                   'width_slider_min': 0,
                                   'width_slider_max': 120,
                                   'width_min_val': width_min,
                                   'width_max_val': width_max,
                                   'depth_slider_min': 0,
                                   'depth_slider_max': 72,
                                   'depth_min_val': depth_min,
                                   'depth_max_val': depth_max,
                                   # 'segments': Segment.objects.all(),
                                   'colors': Color.objects.all(),
                                   'styles': Style.objects.all(),
                                   #'categories': Category.objects.all(),
                                   'furnituretypes': FurnitureType.objects.all(),
                                   'rooms': Room.objects.all(),
                                   'selected_rooms': rooms_ids,
                                   'neighborhoods': Neighborhoods['SF']
                                   }

        if categories:
            context['searchfilter']['categories'] = categories
        if categories_ids:
            context['searchfilter']['selected_categories'] = categories_ids

        if groups:
            context['searchfilter']['groups'] = groups
        if groups_ids:
            context['searchfilter']['selected_groups'] = groups_ids

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


class StyleView(AjaxListView):
    template_name = 'goods/main/shop_ajax.html'
    page_template = 'goods/main/landing_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'

    def get_queryset(self):
        queryset = self.model.objects.filter(is_published=True, pub_date__lte=timezone.now(), store__is_featured=True).exclude(description__isnull=True)

        slug = self.kwargs.get('slug', '')
        try:
            style = Style.objects.get(slug=slug)
        except Style.DoesNotExist:
            raise Http404("Style does not exist")

        queryset = queryset.filter(style=style)


        rooms = None
        if self.request.GET.get('filter-room'):
            rooms = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]
        if (rooms):
            queryset = queryset.filter(room__in=rooms)

        categories = None
        if self.request.GET.get('filter-category'):
            categories = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        if (categories):
            queryset = queryset.filter(category__in=categories)

        colors = None
        if self.request.GET.get('filter-color'):
            colors = [int(i.strip()) for i in self.request.GET.get('filter-color').split(',')]
        if(colors):
            queryset = queryset.filter(color__in=colors)

        # TODO: enable styles, styles are for now disabled
        # styles = [int(i) for i in self.request.GET.getlist('filter-style')]
        # if(styles):
        #    queryset = queryset.filter(style__in=styles)

        furnituretypes = None
        if self.request.GET.get('filter-furnituretype'):
            furnituretypes = [int(i.strip()) for i in self.request.GET.get('filter-furnituretype').split(',')]
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

    def get_context_data(self, **kwargs):
        #print self.request
        context = super(StyleView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY




        categories = None
        categories_ids = []
        groups = None
        rooms_ids = []
        groups_ids = []
        if self.request.GET.get('filter-room'):
            rooms_ids = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]

            rooms = Room.objects.filter(pk__in=rooms_ids)
            #context['rooms'] = rooms

            categories = Category.objects.filter(rooms__in=rooms_ids).distinct()
            context['categories'] = categories
        if self.request.GET.get('filter-category'):
            categories_ids = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        #categories_ids = list(set(categories.distinct().values_list('id', flat=True)))
            groups = Group.objects.filter(categories__in=categories_ids).distinct()
            #context['groups'] = groups

        if self.request.GET.get('filter-group'):
            groups_ids = [int(i.strip()) for i in self.request.GET.get('filter-group').split(',')]

        price_filter = self.request.GET.get('filter-price', None)

        if price_filter:
            price_min = price_filter.split(';')[0]
            price_max = price_filter.split(';')[1]
        else:
            price_min = self.request.GET.get('filter-price-min', 0)
            price_max = self.request.GET.get('filter-price-max', 5000)

        # Filtering height
        height_filter = self.request.GET.get('filter-height', None)
        if height_filter:
            height_min = height_filter.split(';')[0]
            height_max = height_filter.split(';')[1]
        else:
            height_min = self.request.GET.get('filter-height-min', 0)
            height_max = self.request.GET.get('filter-height-max', 72)

        # Filtering width
        width_filter = self.request.GET.get('filter-width', None)
        if width_filter:
            width_min = width_filter.split(';')[0]
            width_max = width_filter.split(';')[1]
        else:
            width_min = self.request.GET.get('filter-width-min', 0)
            width_max = self.request.GET.get('filter-width-max', 120)

        # Filtering depth
        depth_filter = self.request.GET.get('filter-depth', None)
        if depth_filter:
            depth_min = depth_filter.split(';')[0]
            depth_max = depth_filter.split(';')[1]
        else:
            depth_min = self.request.GET.get('filter-depth-min', 0)
            depth_max = self.request.GET.get('filter-depth-max', 72)

        context['searchfilter'] = {
                                   'price_slider_min': 0,
                                   'price_slider_max': price_slider_max,
                                   'price_min_val': price_min,
                                   'price_max_val': price_max,
                                   'height_slider_min': 0,
                                   'height_slider_max': 72,
                                   'height_min_val': height_min,
                                   'height_max_val': height_max,
                                   'width_slider_min': 0,
                                   'width_slider_max': 120,
                                   'width_min_val': width_min,
                                   'width_max_val': width_max,
                                   'depth_slider_min': 0,
                                   'depth_slider_max': 72,
                                   'depth_min_val': depth_min,
                                   'depth_max_val': depth_max,
                                   # 'segments': Segment.objects.all(),
                                   'colors': Color.objects.all(),
                                   'styles': Style.objects.all(),
                                   #'categories': Category.objects.all(),
                                   'furnituretypes': FurnitureType.objects.all(),
                                   'rooms': Room.objects.all(),
                                   'selected_rooms': rooms_ids,
                                   'neighborhoods': Neighborhoods['SF']
                                   }

        if categories:
            context['searchfilter']['categories'] = categories
        if categories_ids:
            context['searchfilter']['selected_categories'] = categories_ids

        if groups:
            context['searchfilter']['groups'] = groups
        if groups_ids:
            context['searchfilter']['selected_groups'] = groups_ids

        context['room_waterfall'] = True

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


class RoomView(AjaxListView):
    template_name = 'goods/main/shop_ajax.html'
    page_template = 'goods/main/landing_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'

    def get_queryset(self):
        queryset = self.model.objects.filter(is_published=True, pub_date__lte=timezone.now(), store__is_featured=True).exclude(description__isnull=True)

        slug = self.kwargs.get('slug', '')
        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            raise Http404("Room does not exist")

        queryset = queryset.filter(room=room)


        #rooms = None
        #if self.request.GET.get('filter-room'):
            #rooms = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]
        #if (rooms):
            #queryset = queryset.filter(room__in=rooms)

        categories = None
        if self.request.GET.get('filter-category'):
            categories = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        if (categories):
            queryset = queryset.filter(category__in=categories)

        colors = None
        if self.request.GET.get('filter-color'):
            colors = [int(i.strip()) for i in self.request.GET.get('filter-color').split(',')]
        if(colors):
            queryset = queryset.filter(color__in=colors)

        # TODO: enable styles, styles are for now disabled
        # styles = [int(i) for i in self.request.GET.getlist('filter-style')]
        # if(styles):
        #    queryset = queryset.filter(style__in=styles)

        furnituretypes = None
        if self.request.GET.get('filter-furnituretype'):
            furnituretypes = [int(i.strip()) for i in self.request.GET.get('filter-furnituretype').split(',')]
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

    def get_context_data(self, **kwargs):
        #print self.request
        context = super(RoomView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY


        slug = self.kwargs.get("slug", "")
        if slug:
            room = Room.objects.get(slug=slug)


        categories = None
        categories_ids = []
        groups = None
        rooms_ids = []
        groups_ids = []
        if self.request.GET.get('filter-room'):
            rooms_ids = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]

            rooms = Room.objects.filter(pk__in=rooms_ids)
            #context['rooms'] = rooms

            categories = Category.objects.filter(rooms__in=rooms_ids).distinct()
            context['categories'] = categories
        if self.request.GET.get('filter-category'):
            categories_ids = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        #categories_ids = list(set(categories.distinct().values_list('id', flat=True)))
            groups = Group.objects.filter(categories__in=categories_ids).distinct()
            #context['groups'] = groups

        if self.request.GET.get('filter-group'):
            groups_ids = [int(i.strip()) for i in self.request.GET.get('filter-group').split(',')]

        price_filter = self.request.GET.get('filter-price', None)

        if price_filter:
            price_min = price_filter.split(';')[0]
            price_max = price_filter.split(';')[1]
        else:
            price_min = self.request.GET.get('filter-price-min', 0)
            price_max = self.request.GET.get('filter-price-max', 5000)

        # Filtering height
        height_filter = self.request.GET.get('filter-height', None)
        if height_filter:
            height_min = height_filter.split(';')[0]
            height_max = height_filter.split(';')[1]
        else:
            height_min = self.request.GET.get('filter-height-min', 0)
            height_max = self.request.GET.get('filter-height-max', 72)

        # Filtering width
        width_filter = self.request.GET.get('filter-width', None)
        if width_filter:
            width_min = width_filter.split(';')[0]
            width_max = width_filter.split(';')[1]
        else:
            width_min = self.request.GET.get('filter-width-min', 0)
            width_max = self.request.GET.get('filter-width-max', 120)

        # Filtering depth
        depth_filter = self.request.GET.get('filter-depth', None)
        if depth_filter:
            depth_min = depth_filter.split(';')[0]
            depth_max = depth_filter.split(';')[1]
        else:
            depth_min = self.request.GET.get('filter-depth-min', 0)
            depth_max = self.request.GET.get('filter-depth-max', 72)

        context['searchfilter'] = {
           'price_slider_min': 0,
           'price_slider_max': price_slider_max,
           'price_min_val': price_min,
           'price_max_val': price_max,
           'height_slider_min': 0,
           'height_slider_max': 72,
           'height_min_val': height_min,
           'height_max_val': height_max,
           'width_slider_min': 0,
           'width_slider_max': 120,
           'width_min_val': width_min,
           'width_max_val': width_max,
           'depth_slider_min': 0,
           'depth_slider_max': 72,
           'depth_min_val': depth_min,
           'depth_max_val': depth_max,
           # 'segments': Segment.objects.all(),
           'colors': Color.objects.all(),
           'styles': Style.objects.all(),
           'categories': Category.objects.filter(rooms=room),
           'furnituretypes': FurnitureType.objects.all(),
           'rooms': Room.objects.all(),
           'selected_rooms': rooms_ids,
           'neighborhoods': Neighborhoods['SF']
           }

        if categories:
            context['searchfilter']['categories'] = categories
        if categories_ids:
            context['searchfilter']['selected_categories'] = categories_ids

        if groups:
            context['searchfilter']['groups'] = groups
        if groups_ids:
            context['searchfilter']['selected_groups'] = groups_ids

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

class CategoryView(AjaxListView):
    template_name = 'goods/main/shop_ajax.html'
    page_template = 'goods/main/landing_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'

    def get_queryset(self):
        queryset = self.model.objects.filter(is_published=True, pub_date__lte=timezone.now(), store__is_featured=True).exclude(description__isnull=True)

        slug = self.kwargs.get('slug', '')
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")

        queryset = queryset.filter(category=category)


        #rooms = None
        #if self.request.GET.get('filter-room'):
            #rooms = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]
        #if (rooms):
            #queryset = queryset.filter(room__in=rooms)

       # categories = None
        #if self.request.GET.get('filter-category'):
            #categories = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        #if (categories):
            #queryset = queryset.filter(category__in=categories)

        colors = None
        if self.request.GET.get('filter-color'):
            colors = [int(i.strip()) for i in self.request.GET.get('filter-color').split(',')]
        if(colors):
            queryset = queryset.filter(color__in=colors)

        # TODO: enable styles, styles are for now disabled
        # styles = [int(i) for i in self.request.GET.getlist('filter-style')]
        # if(styles):
        #    queryset = queryset.filter(style__in=styles)

        furnituretypes = None
        if self.request.GET.get('filter-furnituretype'):
            furnituretypes = [int(i.strip()) for i in self.request.GET.get('filter-furnituretype').split(',')]
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

    def get_context_data(self, **kwargs):
        #print self.request
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY


        slug = self.kwargs.get("slug", "")
        if slug:
            category = Category.objects.get(slug=slug)


        categories = None
        categories_ids = []
        groups = None
        rooms_ids = []
        groups_ids = []
        if self.request.GET.get('filter-room'):
            rooms_ids = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]

            rooms = Room.objects.filter(pk__in=rooms_ids)
            #context['rooms'] = rooms

            categories = Category.objects.filter(rooms__in=rooms_ids).distinct()
            context['categories'] = categories
        if self.request.GET.get('filter-category'):
            categories_ids = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        #categories_ids = list(set(categories.distinct().values_list('id', flat=True)))
            groups = Group.objects.filter(categories__in=categories_ids).distinct()
            #context['groups'] = groups

        if self.request.GET.get('filter-group'):
            groups_ids = [int(i.strip()) for i in self.request.GET.get('filter-group').split(',')]

        price_filter = self.request.GET.get('filter-price', None)

        if price_filter:
            price_min = price_filter.split(';')[0]
            price_max = price_filter.split(';')[1]
        else:
            price_min = self.request.GET.get('filter-price-min', 0)
            price_max = self.request.GET.get('filter-price-max', 5000)

        # Filtering height
        height_filter = self.request.GET.get('filter-height', None)
        if height_filter:
            height_min = height_filter.split(';')[0]
            height_max = height_filter.split(';')[1]
        else:
            height_min = self.request.GET.get('filter-height-min', 0)
            height_max = self.request.GET.get('filter-height-max', 72)

        # Filtering width
        width_filter = self.request.GET.get('filter-width', None)
        if width_filter:
            width_min = width_filter.split(';')[0]
            width_max = width_filter.split(';')[1]
        else:
            width_min = self.request.GET.get('filter-width-min', 0)
            width_max = self.request.GET.get('filter-width-max', 120)

        # Filtering depth
        depth_filter = self.request.GET.get('filter-depth', None)
        if depth_filter:
            depth_min = depth_filter.split(';')[0]
            depth_max = depth_filter.split(';')[1]
        else:
            depth_min = self.request.GET.get('filter-depth-min', 0)
            depth_max = self.request.GET.get('filter-depth-max', 72)

        context['searchfilter'] = {
           'price_slider_min': 0,
           'price_slider_max': price_slider_max,
           'price_min_val': price_min,
           'price_max_val': price_max,
           'height_slider_min': 0,
           'height_slider_max': 72,
           'height_min_val': height_min,
           'height_max_val': height_max,
           'width_slider_min': 0,
           'width_slider_max': 120,
           'width_min_val': width_min,
           'width_max_val': width_max,
           'depth_slider_min': 0,
           'depth_slider_max': 72,
           'depth_min_val': depth_min,
           'depth_max_val': depth_max,
           # 'segments': Segment.objects.all(),
           'colors': Color.objects.all(),
           'styles': Style.objects.all(),
           #'categories': Category.objects.filter(rooms=room),
           'groups': Group.objects.filter(categories=category),
           'furnituretypes': FurnitureType.objects.all(),
           'rooms': Room.objects.all(),
           'selected_rooms': rooms_ids,
           'neighborhoods': Neighborhoods['SF']
           }

        if categories:
            context['searchfilter']['categories'] = categories
        if categories_ids:
            context['searchfilter']['selected_categories'] = categories_ids

        if groups:
            context['searchfilter']['groups'] = groups
        if groups_ids:
            context['searchfilter']['selected_groups'] = groups_ids

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
        # segments = [int(i) for i in self.request.GET.getlist('filter-segment')]
        # if(segments):
        #     queryset = queryset.filter(segment__in=segments)

        # subcategories = [int(i) for i in self.request.GET.getlist('filter-subcategory')]
        # if(subcategories):
        #     queryset = queryset.filter(subcategory__in=subcategories)


        rooms = None
        if self.request.GET.get('filter-room'):
            rooms = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]
        if (rooms):
            queryset = queryset.filter(room__in=rooms)

        categories = None
        if self.request.GET.get('filter-category'):
            categories = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        if (categories):
            queryset = queryset.filter(category__in=categories)

        colors = None
        if self.request.GET.get('filter-color'):
            colors = [int(i.strip()) for i in self.request.GET.get('filter-color').split(',')]
        if(colors):
            queryset = queryset.filter(color__in=colors)

        # TODO: enable styles, styles are for now disabled
        # styles = [int(i) for i in self.request.GET.getlist('filter-style')]
        # if(styles):
        #    queryset = queryset.filter(style__in=styles)

        furnituretypes = None
        if self.request.GET.get('filter-furnituretype'):
            furnituretypes = [int(i.strip()) for i in self.request.GET.get('filter-furnituretype').split(',')]
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

    def get_context_data(self, **kwargs):
        context = super(SearchFilterView, self).get_context_data(**kwargs)
        object_list = context['object_list']

        #rooms_ids = [int(i) for i in self.request.GET.getlist('filter-room')]
        if self.request.GET.get('filter-room'):
            rooms_ids = [int(i.strip()) for i in self.request.GET.get('filter-room').split(',')]

            rooms = Room.objects.filter(pk__in=rooms_ids)
            context['rooms'] = rooms

            categories = Category.objects.filter(rooms__in=rooms_ids).distinct()
            context['categories'] = categories
        if self.request.GET.get('filter-category'):
            categories_ids = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]
        #categories_ids = list(set(categories.distinct().values_list('id', flat=True)))
            groups = Group.objects.filter(categories__in=categories_ids).distinct()
            context['groups'] = groups

        #print self.request.GET
        #if self.request.GET.get('filter-room') and not self.request.GET.get('filter-category'):
            #context['categories'] = categories
        #else:
            #context['categories'] = []

        return context

    def render_to_response(self, context, **kwargs):
        print context.get('page_template')

        response = {}
        context['request'] = self.request
        response['data'] = render_to_string(context.get('page_template'), context)
        #response['data'] =  super(SearchFilterView, self).render_to_response(template_name, **kwargs)
        categories = []
        context_cat = context.get('categories', [])


        categories_ids = []
        if self.request.GET.get('filter-category'):
            categories_ids = [int(i.strip()) for i in self.request.GET.get('filter-category').split(',')]

        print "CCContext"
        print context_cat
        print self.request.GET
        for i in context_cat:
            category = {}
            category['name'] = i.select.capitalize()
            category['id'] = i.id
            if (i.id in categories_ids):
                category['checked'] = True
            categories.append(category)
        if context_cat:
            response['categories'] = categories

        groups = []
        context_groups = context.get('groups', [])


        groups_ids = []
        if self.request.GET.get('filter-group'):
            groups_ids = [int(i.strip()) for i in self.request.GET.get('filter-group').split(',')]

        for i in context_groups:
            group = {}
            group['name'] = i.select.capitalize()
            group['id'] = i.id
            if (i.id in groups_ids):
                group['checked'] = True
            groups.append(group)
        if context_cat:
            response['groups'] = groups

        return HttpResponse(json.dumps(response), content_type="application/json")
        return response


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
        context['product_slug'] = product.slug
        product_click = ProductClick()
        product_click.product = product



        # click counter
        exclude_emails = settings.CLICK_EXCLUSIONS
        if(self.request.user.is_authenticated()):
            if not self.request.user.email in exclude_emails:
                product_click.user = self.request.user
                product.click_count += 1
                product.save()
                logger.debug('added to click-count')
        else:
            product.click_count += 1
            product.save()
            logger.debug('added to click-count')

        product_click.save()
        logger.debug('Product Click event saved')
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
