from django.views import generic
from goods.models import Product, Category, FurnitureType, Segment, ProductImage
from members.models import AuthUserActivity, OfferType, PromotionOffer
from django.core.serializers import serialize
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
# from goods.forms import CommentForm
from random import randint
import logging
from django.conf import settings
from random import shuffle
from helper import is_time_to_show_modal, hide_modal
import uuid

# from helper import get_liked_items

from pprint import pprint as pp

from endless_pagination.views import AjaxListView



logger = logging.getLogger(__name__)

BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'


class LandingView(generic.ListView):
    template_name = 'goods/landing/landing.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        queryset = self.model.objects.filter(is_landing=True, store__is_featured=True)[:6]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)

        if(not self.request.session.get('cid', None)):
            self.request.session['cid'] = str(uuid.uuid4())

        context['BaseUrl'] = BASE_URL
        if(settings.ENABLE_REFERRAL):
            if(self.request.user.is_authenticated()):
                if(is_time_to_show_modal(self.request, 'referral2')):
                    logger.info('we should be showing 2nd modal')
                    context['show_referral_second_modal'] = True
                    hide_modal(self.request, 'referral2', settings.SECOND_REFERRAL_MODAL_EXP)
            else:
                if(is_time_to_show_modal(self.request, 'referral1')):
                    logger.info('we should be showing 1st modal')
                    context['show_referral_first_modal'] = True
                    hide_modal(self.request, 'referral1', settings.FIRST_REFERRAL_MODAL_EXP)


        context['SIGNUP_OFFER'] = settings.SIGNUP_OFFER

        # add any "First time" offers
        #only FIRST_ORDERs. DISCOUNT_PROMOs arent rendered
        # if there is more than one get the first one
        print('show_modal: ', is_time_to_show_modal(self.request, 'offer_modal'))
        if(is_time_to_show_modal(self.request, 'offer_modal')):
#         if(not self.request.session.get('seen_offers', False)):
            offers = PromotionOffer.get_current_offers(user=self.request.user, offer_type=OfferType.FIRST_ORDER)
            print('offers:', offers)
            if(offers):
                context['promotion_offer'] = offers[0]

                # seen_offers flag in session will tell us next time
                # whether we should show this offer or not
                # expiration is needed so that after this flag expires
                # we will show the offer again
                hide_modal(self.request, 'offer_modal', settings.OFFER_MODAL_EXPIRATION)
#                 self.request.session['seen_offers'] = True
#                 self.request.session.set_expiry(settings.OFFER_MODAL_EXPIRATION)

        return context


class LandingTestView(AjaxListView):
    template_name = 'goods/landingtest/landingtest_ajax.html'
    page_template = 'goods/landingtest/landingtest_ajax_page.html'
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
        context = super(LandingTestView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'goods/detail/detail.html'
    context_object_name = 'product'
    model = Product
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['returns'] = settings.RETURN_POLICY
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

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
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
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
