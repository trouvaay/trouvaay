from django.http import JsonResponse
from django.views import generic
from members.models import AuthUserActivity, AuthUser, \
    AuthUserAddress, RegistrationProfile, \
    PromotionOffer, Join, Profile, AuthOrder, OrderType, \
    Reservation, OrderAddress, Purchase, Redemption, Offer
from goods.models import Product
from members.forms import CustomAuthenticationForm, RegistrationForm, \
    ReserveForm, ReserveFormAuth, ReferralForm, PostCheckoutForm
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import stripe
from django.shortcuts import redirect
from django.conf import settings
import logging
from datetime import datetime, timedelta
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login
from registration import signals
from helper import get_site, send_order_email, send_user_password_change_email
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout
from django.shortcuts import render_to_response
from django.http import HttpResponse
from decimal import Decimal
from urllib import urlencode
import hashlib
import random


logger = logging.getLogger(__name__)

# TODO: For profile page
class ProfileView(LoginRequiredMixin, generic.DetailView):
    """Displays user profile"""

    template_name = 'members/closet/closet.html'
    context_object_name = 'user'
    model = AuthUser

    def get_object(self):
        """Returns the object that this view is working with"""

        if (self.request.user.is_authenticated()):
            try:

                user_id = self.request.user.id
                return AuthUser.objects.get(pk= user_id)
            except Exception, e:
                return None
        else:
            return None

    def get_context_data(self, **kwargs):
        """Returns context for template for this view"""

        context = super(ProfileView, self).get_context_data(**kwargs)
        user = self.get_object()
        ordered_items = Product.objects.filter(product_orders__in=user.user_orders.filter(order_type=OrderType.RESERVATION_ORDER,
                                                                                          reservation__is_active=True))
        print ordered_items.query
        context['user_order_items'] = ordered_items
        print (context['user_order_items'])
        user_activity = AuthUserActivity.objects.get(authuser=user)
        
        # diff from liked_items context function in context_processors.py
        context['liked_products'] = user_activity.saved_items.exclude(id__in=[i.id for i in ordered_items])
        context['OFFER_IS_ENABLED'] = settings.OFFER_IS_ENABLED
        return context


class SignupView(BaseRegistrationView):
    """Handles user signup process"""

    template_name = 'registration/registration_form.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """Returns the context for the template for this view"""

        context = super(SignupView, self).get_context_data(**kwargs)
        context['signup_form'] = RegistrationForm()
        context['login_form'] = RegistrationForm()

        return context

    def register(self, request, **cleaned_data):
        """Creates user"""

        email = cleaned_data['email']
        password = cleaned_data.get('password', None)
        need_password_reset = False
        if(password is None):
            need_password_reset = True
            # need something for the password
            # we will hash email, timestamp and a random number
            random.seed()
            password = hashlib.sha256('{0}|{1}|{2}'.format(email, timezone.now(), random.randint(0, 1000000000))).hexdigest()

        site = get_site(request)
        new_user = RegistrationProfile.objects.create_active_user(
            email, password, site,
            send_email=False,
            request=request,
        )
        user = authenticate(email=email, password=password)
        login(request, user)
        signals.user_activated.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        Join.create_join(request, user)
        Profile.create_profile(user)
        if(need_password_reset):
            send_user_password_change_email(request, new_user)
        return new_user


class AjaxLoginView(generic.TemplateView):
    """Displays login/signup forms that can be loaded via ajax"""
    
    template_name = "members/auth/ajax_signup_login.html"
    
    def get_context_data(self, **kwargs):

        if(self.request.user.is_authenticated()):
            django_logout(self.request)

        context = super(AjaxLoginView, self).get_context_data(**kwargs)
        context['login_form'] = CustomAuthenticationForm()
        context['signup_form'] = RegistrationForm()
        context['social_login'] = settings.ENABLE_SOCIAL_AUTH
        return context
    

def ProductLike(request):
    """Adds product instance to 'saved_items' field of 
        AuthUserActivity model
    """
    # because this is called via AJAX, the @login_required decorator
    # is not very useful, so instead we have to manually check if
    # user is authenticated or not and return appropariate status in json

    if(not request.user.is_authenticated()):
        return JsonResponse('loginrequired', safe=False)

    if request.method == "POST":
        userinstance = request.user
        product = Product.objects.get(pk=int(request.POST['id']))
        useractivity = AuthUserActivity.objects.get(authuser=userinstance)
        if product in useractivity.saved_items.all():
            useractivity.saved_items.remove(product)
        else:
            useractivity.saved_items.add(product)
        useractivity.save()
        return JsonResponse('success', safe=False)
    else:
        return JsonResponse('success', safe=False)


def CancelReserve(request):
    """Remove product from reserve in Profile"""
    # because this is called via AJAX, the @login_required decorator
    # is not very useful, so instead we have to manually check if
    # user is authenticated or not and return appropariate status in json

    if(not request.user.is_authenticated()):
        return JsonResponse('loginrequired', safe=False)

    if request.method == "POST":
        userinstance = request.user
        product_id = int(request.POST['id'])

        # using filter here instead of get
        # because found the cases where
        # there were multiple reservations
        # of the same item by the same user
        # so we need to cancel all of them
        reservations = Reservation.objects.filter(authuser=request.user,
                                                  order__product__id=product_id,
                                                  is_active=True)
        for reservation in reservations:
            reservation.cancel_reservation()
            logger.debug('canceled reservation {0}'.format(reservation.id))

    return JsonResponse('success', safe=False)


class ReferralSignup(generic.edit.FormView):
    """Creates user via referral"""

    template_name = 'members/referral/signup.html'
    # form_class = ReferralForm
    form_class = RegistrationForm
    success_url = reverse_lazy('members:referral_info')

    def form_valid(self, form):
        """Handles referral signup, this is called when submitted form was validated"""

        email = form.cleaned_data['email']
        self.success_url += "?"
        self.success_url += urlencode({'email': email})
        is_existing, user = get_user_model().get_user_by_email(email)
        if(not is_existing):
            send_user_password_change_email(self.request, user)
        Join.create_join(self.request, user)
        return super(ReferralSignup, self).form_valid(form)


class ReferralInfo(generic.base.TemplateView):
    """Shows user referral link which they can give to others to signup"""

    template_name = 'members/referral/info.html'

    def get_context_data(self, **kwargs):
        """Returns conext for template for this view"""

        context = super(ReferralInfo, self).get_context_data(**kwargs)
        user = None
        if(self.request.user.is_authenticated()):
            user = self.request.user
        else:
            email = self.request.GET.get('email', None)
            if(email):
                is_existing, user = get_user_model().get_user_by_email(email)
                if(not is_existing):
                    send_user_password_change_email(self.request, user)

        if(user):
            Join.create_join(self.request, user)
            context['ref_url'] = user.get_referral_link()
        return context

class ReserveView(generic.DetailView):
    """Precheckout and Postcheckout combined"""

    context_object_name = 'product'
    model = Product

    def __can_reserve(self, product, user):
        """Checks if this user can reserve this product.
        
        Returns tuple
        (status, message)
        where
            status - boolean, True - yes this user can reserve, False - user cannot reserve
            message - string, in case user cannot reserve this it contains message why not, 
            otherwise empty string
        """

        # make sure user is not trying to reserve an item that is already reserved or sold
        if(product.is_sold):
            return (False, "Sorry this item is no longer available")
        elif(product.is_reserved):
            # need to check who reserved the item to give a user an appropriate message
            if(user.is_authenticated() and
               user.user_orders.filter(order_type=OrderType.RESERVATION_ORDER,
                                       reservation__is_active=True,
                                       product=product).count() > 0):
                return (False, "You've already reserved this item, you can see all your reservations in your profile page.")
            else:
                return (False, "Sorry this item is currently reserved")
        return (True, '')

    def get(self, request, *args, **kwargs):
        """Shows the reservation form"""

        product = self.get_object()

        can_reserve_check, reservation_message = self.__can_reserve(product, request.user)
        if(not can_reserve_check):
            return render_to_response('members/purchase/reserve_postcheckout.html', locals())


        form = None
        if(request.user.is_authenticated()):
            # make sure user has the profile
            Profile.create_profile(request.user)
            form = ReserveFormAuth(initial={'first_name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'phone': request.user.profile.phone
                                            })
        else:
            form = ReserveForm()

        return render_to_response('members/purchase/reserve_precheckout.html', locals())

    def post(self, request, *args, **kwargs):
        """Completes the reservation process"""

        product = self.get_object()
        order_user = None
        if(request.user.is_authenticated()):

            form = ReserveFormAuth(request.POST)
            if(not form.is_valid()):
                return render_to_response('members/purchase/reserve_precheckout.html', locals())

            order_user = request.user
            # Used as param in send_order_email fct
            is_existing = True

        else:        
            form = ReserveForm(request.POST)
            if(not form.is_valid()):
                return render_to_response('members/purchase/reserve_precheckout.html', locals())
    
            # create user if needed
            email = self.request.POST.get('email', None)
            is_existing, order_user = get_user_model().get_user_by_email(email)
            logger.debug('is_existing: {}'.format(is_existing))            

            update_user = False
            first_name = form.cleaned_data['first_name']
            if(not first_name is None):
                order_user.first_name = first_name
                update_user = True
            last_name = form.cleaned_data['last_name']
            if(not last_name is None):
                order_user.last_name = last_name
                update_user = True
            if(update_user):
                order_user.save()
            phone = form.cleaned_data['phone']
            if(not phone is None):
                profile = order_user.profile
                profile.phone = phone
                profile.save()
        
        # If new user need to set send_password link param to true 
        if is_existing:
            password_reset_link = False
        else:
            password_reset_link = True
            Join.create_join(self.request, order_user)

        logger.debug('Generate password rest?: {}'.format(password_reset_link))
        logger.debug('number of reservations that user already has: %d' % order_user.get_number_of_reservations())
        logger.debug('reservations limit in settings: %d' % settings.RESERVATION_LIMIT)
        if(order_user.get_number_of_reservations() >= settings.RESERVATION_LIMIT):
            reservation_message = "Sorry it looks like you've hit your reservation limit - save something for the rest of us!.  On a serious note email us to extend your limit and we're generally happy to accomodate.  Unless you're a robot..."
            return render_to_response('members/purchase/reserve_postcheckout.html', locals())

        can_reserve_check, reservation_message = self.__can_reserve(product, order_user)
        if(not can_reserve_check):
            return render_to_response('members/purchase/reserve_postcheckout.html', locals())

        # create order
        order = AuthOrder()
        order.authuser = order_user
        order.product = product
        order.order_type = OrderType.RESERVATION_ORDER
        order.converted_from_reservation = False
        order.save()
        logger.debug('created AuthOrder')

        # create reservation
        Reservation.create_reservation(order)
        
        logger.debug('product is_reserved field set to True')

        # send order confirmation email
        send_order_email(request=self.request, order=order, show_password_reset_link=password_reset_link, is_buy=False)
        return render_to_response('members/purchase/reserve_postcheckout.html', locals())
                

class BuyView(generic.DetailView):
    """Pre-checkout and post-checkout for the buying process"""

    context_object_name = 'product'
    model = Product

    def __create_or_update_default_address(self, request, user):
        """Creates if needed or updated existing default user address"""

        default_address = None
        if(hasattr(user, 'default_address')):
            default_address = user.default_address
        else:
            default_address = AuthUserAddress()

        default_address.authuser = user
        default_address.street = request.POST['args[shipping_address_line1]']
        default_address.city = request.POST['args[shipping_address_city]']
        default_address.state = request.POST['args[shipping_address_state]']
        default_address.zipcd = request.POST['args[shipping_address_zip]']
        default_address.shipping = True
        default_address.save()

    def __can_buy(self, product, user):
        """Checks if this user can buy this product.
        
        Returns tuple
        (status, message)
        where
            status - boolean, True - yes this user can buy, False - user cannot reserve
            message - string, in case user cannot buy this product, it contains message 
            why not, otherwise empty string
        """

        # make sure user is not trying to buy an item that is already reserved or sold
        if(product.is_sold):
            return (False, "Sorry this item is no longer available")
        elif(product.is_reserved):
            # need to check who reserved the item to give a user an appropriate message
            if(user.is_authenticated() and
               user.user_orders.filter(order_type=OrderType.RESERVATION_ORDER,
                                       reservation__is_active=True,
                                       product=product).count() > 0):
                # this item is reserved by this user, now they can buy it
                return (True, '')
            else:
                return (False, "Sorry this item is currently reserved")
        return (True, '')

    def __create_order_address(self, request, order):
        """Creates order address from request's shipping address"""

        order_address = OrderAddress()
        order_address.order = order
        order_address.street = request.POST['args[shipping_address_line1]']
        order_address.city = request.POST['args[shipping_address_city]']
        order_address.state = request.POST['args[shipping_address_state]']
        order_address.zipcd = request.POST['args[shipping_address_zip]']
        order_address.shipping = True
        order_address.save()

    def __update_name(self, request, user):
        """Update user's first and last name if needed"""

        update_user = False
        first_name = None
        last_name = None
        if(not user.first_name or not user.last_name):
            full_name = self.request.POST.get('args[shipping_name]', None)
            if(full_name):
                if(' ' in full_name):
                    first_name, last_name = full_name.strip().split(' ', 1)
                else:
                    first_name = full_name.strip()
        if(not user.first_name and first_name):
            user.first_name = first_name
            update_user = True
        if(not user.last_name and last_name):
            user.last_name = last_name
            update_user = True
        if(update_user):
            user.save()

    def __process_stripe_create_order(self):
        pass

    def __check_offer(self, request, *args, **kwargs):
        """Checks the offer and determines if it is accepted or rejected
        
        returns tuple: (is_offer, offer_price, is_offer_accepted, offer_header, offer_message)
        where
            is_offer - boolean, True - request contains an offer, False - otherwise
            offer_price - Decimal, dollar amount of the offer, or None if offer is invalid
            is_offer_accepted - boolean, offer in the request is accepted, False otherwise
            offer_header - in case offer is rejected this contaisn the header of the modal that should be shown to user
            offer_message - in case offer is rejected this is a message containing reason why
        """

        product = self.get_object()

        is_offer = False
        offer_price = None
        is_offer_accepted = False
        offer_header = None
        offer_message = None
        
        if('is_offer' in kwargs.keys() and kwargs['is_offer']):
            is_offer = True

        if(is_offer):
            if(product.minimum_offer_price is None):
                offer_header = "Sorry this retailer isnt accepting offers on this product"
                offer_message = "This product does not accept offers only fixed price."
                return is_offer, offer_price, is_offer_accepted, offer_header, offer_message
    
            if(request.method == 'GET'):
                offer_price = request.GET.get('offer_price', None)
            elif(request.method == 'POST'):
                offer_price = request.POST.get('offer_price', None)
            if(offer_price is None):
                offer_header = "No Offer Submitted"
                offer_message = "Please submit offer price."
                return is_offer, offer_price, is_offer_accepted, offer_header, offer_message
    
            try:
                offer_price = Decimal(offer_price)
            except:
                offer_header = "Offer Rejected"
                offer_message = "Invalid offer amount"
                return is_offer, offer_price, is_offer_accepted, offer_header, offer_message
    
            if(offer_price < product.minimum_offer_price):
                offer_header = "Offer Rejected"
                offer_message = "Sorry your offer was rejected because it is too low."
                return is_offer, offer_price, is_offer_accepted, offer_header, offer_message

            is_offer_accepted = True
        
        return is_offer, offer_price, is_offer_accepted, offer_header, offer_message
            
    def get_object(self):
        """Returns the object that this view is working with"""

        product_id = None
        if(self.request.method == "POST"):
            product_id = self.request.POST.get('product_id', None)
        elif(self.request.method == "GET"):
            product_id = self.request.GET.get('product_id', None)
        if(not product_id):
            return None
        try:
            return Product.objects.get(pk=int(product_id))
        except Product.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        """Handles Pre-checkout screen to display order info: 
        price, taxes, promo code (with verification), discounts and total
        """

        product = self.get_object()

        can_buy_status, buy_notavailable_message = self.__can_buy(product, request.user)
        if(not can_buy_status):
            return render_to_response('members/purchase/buy_notavailable.html', locals())

        is_offer, offer_price, is_offer_accepted, buy_notavailable_header, buy_notavailable_message = self.__check_offer(request, *args, **kwargs)
        if(is_offer and offer_price and not is_offer_accepted):
            return render_to_response('members/purchase/buy_notavailable.html', locals())

        promo_code = self.request.GET.get('promo_code', None)
        promo_is_valid = False
        promo_code_message = ''
        promo_codes = []
        if(promo_code):
            promo_is_valid, proper_promo_code, invalid_message = PromotionOffer.is_valid_promo_code(self.request.user, promo_code)
            if(promo_is_valid):
                promo_codes = [proper_promo_code]
                promo_code = proper_promo_code
            else:
                promo_code_message = invalid_message

        total_price_before_offers = product.current_price
        if(is_offer and offer_price):
            total_price_before_offers = offer_price

        discounts, subtotal_dollar_value, taxes, total = Purchase.compute_order_line_items(user=self.request.user,
                                                                                           total_price_before_offers=total_price_before_offers,
                                                                                           promo_codes=promo_codes)
        total_discount = 0
        for discount in discounts:
            total_discount += discount['dollar_value']
        capture_time = timezone.now()
        stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        feature_name_reserve = settings.FEATURE_NAME_RESERVE
        site_name = settings.SITE_NAME

        return render_to_response('members/purchase/buy_precheckout.html', locals())

    def post(self, request, *args, **kwargs):
        """Completes the order after user is done with stripe"""

        try:

            product = self.get_object()

            can_buy_status, buy_notavailable_message = self.__can_buy(product, request.user)
            if(not can_buy_status):
                return JsonResponse({'status': 'error', 'message': buy_notavailable_message})

            order_type = request.POST['order_type'].strip().lower()
            
            # if user already has a reservation for this product
            # use that order, otherwise create new order 
            order = None
            if(self.request.user.is_authenticated()):
                
                try:
                    order = AuthOrder.objects.get(authuser = self.request.user,
                                                  order_type=OrderType.RESERVATION_ORDER,
                                                  reservation__is_active=True,
                                                  product = product)
                    logger.debug('found existing reservation order')

                except AuthOrder.DoesNotExist:
                    # user does not have a reservation for this product, that's ok
                    pass
            if(order is None):
                order = AuthOrder()
                logger.debug('new order')
            
            # create charge with stripe,
            try:
                token_id = request.POST['token[id]']
                total_amount_in_cents = int(request.POST['total_amount'])

                logger.debug('total_amount_in_cents %d' % total_amount_in_cents)
                promo_codes = []
                promo_codes_param = request.POST['promo_codes'].strip()
                if(promo_codes_param):
                    promo_codes = [i for i in promo_codes_param.split(',')]

                total_price_before_offers = product.current_price
                is_offer, offer_price, is_offer_accepted, _header, _message = self.__check_offer(request, *args, **kwargs)

                if(is_offer_accepted):
                    total_price_before_offers = offer_price

                discounts, subtotal_dollar_value, taxes, total = Purchase.compute_order_line_items(user=self.request.user,
                                                                                                   total_price_before_offers=total_price_before_offers,
                                                                                                   promo_codes=promo_codes)
                logger.debug('discounts %s' % str(discounts))
                logger.debug('subtotal_dollar_value %s' % str(subtotal_dollar_value))
                logger.debug('total %s' % str(total))
                logger.debug('total %s' % str(total_amount_in_cents))

                if(total_amount_in_cents != total['in_cents']):
                    # either product price has changed since payment or
                    # user is trying to do something nasty
                    # in any case we have a discrepancy between
                    # what was shown to the user at the time of checkout
                    # and current product price
                    # it is best to stop right here and refresh the page
                    logger.info('Product price did not match the total that came in the request')
                    return JsonResponse({'status': 'error', 'message': 'Total ammount does not match.'})

                order_user = self.request.user
                is_existing = True
                if(not order_user.is_authenticated()):
                    email = self.request.POST.get('token[email]', None)
                    if(not email):
                        # cannot go any further without email
                        logger.info('No email in the request')
                        return JsonResponse({'status': 'error', 'message': 'No email'})
                    is_existing, order_user = get_user_model().get_user_by_email(email)
                    if(not is_existing):
                        Join.create_join(self.request, order_user)

                    logger.debug('is_existing: %s' % str(is_existing))

                # update first ane last name if needed
                self.__update_name(request, order_user)

                Profile.create_profile(order_user)
                order.authuser = order_user
                order.product = product
                if(order.id and order.order_type == OrderType.RESERVATION_ORDER):
                    order.converted_from_reservation = True
                    logger.debug('converting existing reservation order {0} to purchase'.format(order.id))
                else:
                    order.converted_from_reservation = False

                if(is_offer_accepted):
                    order.order_type = OrderType.OFFER_ORDER
                else:
                    order.order_type = OrderType.PURCHASE_ORDER

                order.save()
                logger.debug('saved order {0}'.format(order.id))

                # create redemptions
                for discount in discounts:
                    Redemption.create_redemption(order=order,
                                                 product=product,
                                                 offer_id=discount['offer_id'],
                                                 discount_dollar_value=discount['dollar_value'])

                # create/update addresses
                self.__create_or_update_default_address(self.request, order_user)
                self.__create_order_address(request, order)

                # complete the order by creating Purchase or Offer
                do_order_capture = True
                if(is_offer_accepted):
                    do_order_capture = False
                    Offer.create_offer(order=order, taxes=taxes['dollar_value'], transaction_price=total['in_dollars'], offer_price=offer_price)
                else:
                    Purchase.create_purchase(order=order, taxes=taxes['dollar_value'], transaction_price=total['in_dollars'])

                # create credit card charge with stripe
                stripe.api_key = settings.STRIPE_SECRET_KEY
                stripe.Charge.create(
                    amount=total_amount_in_cents,
                    currency="usd",
                    description=product.short_name,
                    card=token_id,
                    capture=do_order_capture,
                    receipt_email=order_user.email,
                    metadata={
                        'order_id': order.id,
                        'order_type': 'buy' if do_order_capture else 'offer'
                        })

            except Exception, e:
                logger.error('Error in BuyView.post()')
                logger.error(str(e))
                return JsonResponse({'status': 'error', 'message': 'Failed to charge credit card.'})

            # send order confirmation email
            send_order_email(request=self.request, 
                             order=order,
                             show_password_reset_link=(not is_existing),
                             is_buy=True)

            json_result = {
                'status': 'ok',
                'product_name': product.short_name,
                'store_name': product.store.retailer.short_name,
                'store_street': product.store.street,
                'store_street2': product.store.street2 if product.store.street2 else '',
                'store_city': product.store.city,
                'store_state': product.store.state,
                'store_zipcode': product.store.zipcd,
                'ask_phone': False,
                'is_offer': is_offer_accepted
            }

            if(not order.authuser.profile.phone):

                logger.debug("ask for the phone on post checkout")

                # we don't have the phone for this user, need to ask for it
                # if user is non-authenticated, and we are going to ask for the phone number
                # we don't want to allow anyone to simply modify anyone else's phone
                # to prevent that we'd compute this hash
                # when the client submits the phone number the hash has to match with
                # what we compute here
                json_result['ask_phone'] = True
                json_result['email'] = order.authuser.email
                json_result['post_checkout_hash'] = AuthUser.compute_post_checkout_hash(order.authuser)
            else:
                logger.debug("already have a phone number do not ask again")

            return JsonResponse(json_result)
            
        except Exception, e:
            logger.error('Error in BuyView.post()')
            logger.error(str(e))
            return JsonResponse({'status': 'error', 'message': 'Error processing the order.'})


class PostCheckoutUpdate(generic.edit.FormView):
    template_name = 'members/purchase/post_checkout_update_phone.html'
    form_class = PostCheckoutForm
    success_url = None

    def form_valid(self, form):
        user = None
        if(self.request.user.is_authenticated()):
            user = self.request.user
        else:
            email = form.cleaned_data['email']
            post_checkout_hash = form.cleaned_data['post_checkout_hash']
            try:
                find_user = AuthUser.objects.get(email=email)
                real_hash = AuthUser.compute_post_checkout_hash(find_user)
                if(real_hash == post_checkout_hash):
                    user = find_user
            except AuthUser.DoesNotExist:
                # there is no user with this email something abnormal is going on
                logger.error('got email for a non-existing user in PostCheckoutUpdate: {0}'.format(email))
                pass

        if(user):
            profile = user.profile
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return HttpResponse('')


def can_reserve(request):
    """Checks for permissions whether user is able to reserve a product.
    """
    
    if(request.user.is_authenticated()):
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'login_required'})
    

@sensitive_post_parameters()
@csrf_protect
@never_cache
def custom_login(request, template_name='registration/login.html',
          authentication_form=CustomAuthenticationForm):
    """This is a wrapper for django's login view.
    It allows us to pass "next" parameter properly.
    
    """

    # the foolowing unbound instances of forms are needed
    # only for rendering of the template by login 'GET'
    # the actual login 'POST' will be using authentication_form
    # from above
    print('social auth settings', settings.ENABLE_SOCIAL_AUTH)
    extra_context = {
                     'login_form': CustomAuthenticationForm(),
                     'signup_form': RegistrationForm(),
                     'social_login': settings.ENABLE_SOCIAL_AUTH,
                     }
    if request.method == "GET":
        next_param = request.GET.get('next', None)
        if(next_param):
            extra_context = {
                             'login_form': CustomAuthenticationForm(initial={'next':next_param}),
                             'signup_form': RegistrationForm(),
                             'social_login': settings.ENABLE_SOCIAL_AUTH,
                             }
    print 
    return django_login(request=request,
                        template_name=template_name,
                        authentication_form=authentication_form,
                        extra_context=extra_context)


#########Unused Cart Feature ###################

# @login_required
# def AddToCart(request):

#     if request.method == "POST" and request.is_ajax:
#         userinstance = request.user
#         product = Product.objects.get(pk=int(request.POST['id']))
#         usercart, created = AuthUserCart.objects.get_or_create(authuser=userinstance)
#         usercart.saved_items.add(product)
#         usercart.save()
#         count = usercart.get_item_count()
#         return JsonResponse({'count': count, 'message':'success'})
#     else:
#         return JsonResponse('success', safe=False)
        
# class CheckoutView(LoginRequiredMixin, generic.TemplateView):
#     template_name = 'members/purchase/checkout.html'

# @login_required
# def RemoveFromCart(request):

#     if request.method == "POST" and request.is_ajax:
#         userinstance = request.user
#         product = Product.objects.get(pk=int(request.POST['id']))
#         usercart = AuthUserCart.objects.get(authuser=userinstance)
#         usercart.saved_items.remove(product)
#         usercart.save()
#         count = usercart.get_item_count()
#         total = usercart.get_cart_total()
#         return JsonResponse({'count': count, 'total': total, 'id':product.id})
#     else:
#         return JsonResponse('success', safe=False)


# class CartView(LoginRequiredMixin, generic.DetailView):
#     template_name = 'members/purchase/cart.html'
#     context_object_name = 'cart'
#     model = AuthUserCart

#     def get_object(self, queryset=None):
#         return AuthUserCart.objects.get(authuser=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super(CartView, self).get_context_data(**kwargs)
#         context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

#         # TODO: do not add 'site_name' to context
#         # once the 'sites' are setup in settings
#         context['site_name'] = settings.SITE_NAME
#         return context


# class CartCheckoutCallbackView(LoginRequiredMixin, generic.DetailView):
#     template_name = 'members/purchase/cart.html'
#     context_object_name = 'cart'
#     model = AuthUserCart

#     def get_object(self, queryset=None):
#         return AuthUserCart.objects.get(authuser=self.request.user)

#     def post(self, request, *args, **kwargs):
#         try:
#             # create new order
#             order = AuthUserOrder()
#             order.authuser = self.request.user
#             order.save()
#             logger.debug('Created new order %d' % order.id)

#             cart = self.get_object()

#             order_type = request.POST['order_type'].strip().lower()
#             capture_order = (order_type == 'buy')

#             # create charge with stripe,
#             try:
#                 token_id = request.POST['token[id]']
#                 total_amount_in_cents = int(request.POST['total_amount'])

#                 if(total_amount_in_cents != cart.get_cart_total_in_cents()):
#                     # either cart has changed since payment or
#                     # user is trying something nasty
#                     # in any case we have a discrepancy between
#                     # what was shown to the user at the time of checkout
#                     # and current cart contents
#                     # it is best to stop right here and refresh the cart
#                     # so that user can checkout again
#                     logger.info('Cart total did not match the total that came in the request')
#                     return JsonResponse({'status': 'error', 'message': 'Total ammount does not match.'})

#                 order_type = request.POST['order_type']
#                 stripe.api_key = settings.STRIPE_SECRET_KEY
#                 stripe.Charge.create(
#                                     amount=total_amount_in_cents,
#                                     currency="usd",
#                                     card=token_id,
#                                     capture=capture_order,
#                                     metadata={
#                                             'order_id': order.id,
#                                             'order_type': order_type
#                                             })

#             except Exception, e:
#                 logger.error('Error in CartCheckoutCallbackView.post()')
#                 logger.error(str(e))
#                 return JsonResponse({'status': 'error', 'message': 'Failed to charge credit card.'})

#             # create or update shipping address
#             #
#             # TODO: allow multiple addresses per user
#             # right now there is only one address per user which
#             # is enforced in the database with a Unique key on user id
#             shipping_address = None
#             try:
#                 shipping_address = AuthUserAddress.objects.get(authuser=self.request.user)
#                 logger.debug('Updating existing shipping address')
#             except AuthUserAddress.DoesNotExist:
#                 # no address, that's ok we will create a new one
#                 shipping_address = AuthUserAddress()
#                 logger.debug('Creating new shipping address')

#             # TODO: shipping address should be tied to the order
#             # right not it is only tied to user
#             shipping_address.authuser = self.request.user
#             shipping_address.street = request.POST['args[shipping_address_line1]']
#             shipping_address.city = request.POST['args[shipping_address_city]']
#             shipping_address.state = request.POST['args[shipping_address_state]']
#             shipping_address.zipcd = request.POST['args[shipping_address_zip]']
#             shipping_address.shipping = True
#             shipping_address.save()

#             # add items to order
#             for product in cart.saved_items.all():
#                 order_item = AuthUserOrderItem()
#                 order_item.product = product
#                 order_item.order = order
#                 order_item.sell_price = product.current_price
#                 order_item.captured = capture_order
#                 if(capture_order):
#                     order_item.capture_time = timezone.now()
#                 else:
#                     order_item.capture_time = timezone.now() + timedelta(hours=settings.STRIPE_CAPTURE_TRANSACTION_TIME)
#                 order_item.quantity = 1
#                 order_item.save()
#             logger.debug('Added items to order')

#             # all items have been saved in the order now remove them from the cart
#             # TODO: once the item is purchased the total available quantity should be adjusted
#             # which we don't keep track of right now anywhere
#             for product in cart.saved_items.all():
#                 cart.saved_items.remove(product)
#                 logger.debug('removing from cart %s' % str(order_item.product))
#             cart.save()
#             logger.debug('Removed items from cart')

#             return JsonResponse({'status': 'ok', 'message': 'Order is completed.'})
#         except Exception, e:
#             logger.error('Error in CartCheckoutCallbackView.post()')
#             logger.error(str(e))
#             return JsonResponse({'status': 'error', 'message': 'Error processing the order.'})
