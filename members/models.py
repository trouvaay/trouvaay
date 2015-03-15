from localflavor.us.models import (
    PhoneNumberField,
    USStateField,
    )

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
    BaseUserManager
    )
from django.db import models
from django.db.models import Q
from django.conf import settings
from helper import States, get_client_id
from registration.models import RegistrationManager as BaseRegistrationManager
from registration.models import RegistrationProfile as BaseRegistrationProfile
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import hashlib
import six
import random
from datetime import timedelta
import uuid
import logging


logger = logging.getLogger(__name__)

class RegistrationManager(BaseRegistrationManager):

    def create_inactive_user(self, email, password,
                             site, send_email=True, request=None):
        """
        Overwiding the method from the base class to not use the username.
        
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        Additionally, if email is sent and ``request`` is supplied,
        it will be passed to the email template.

        """
        new_user = get_user_model().objects.create_user(email, password)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site, request)

        return new_user

    def create_active_user(self, email, password,
                             site, send_email=True, request=None):
        """
        Overwiding the method from the base class to not use the username.
        
        Create a new, active ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, a confirmation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        Additionally, if email is sent and ``request`` is supplied,
        it will be passed to the email template.

        """
        new_user = get_user_model().objects.create_user(email, password)
        new_user.is_active = True
        new_user.save()

        

        #Need to update - currently sends activation email
        # if send_email:
        #     registration_profile.send_activation_email(site, request)

        return new_user

    def create_profile(self, user):
        """
        Overwiding the method from the base class to not use the username.
        
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.

        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.

        """
        salt = hashlib.sha1(six.text_type(random.random()).encode('ascii')).hexdigest()[:5]
        salt = salt.encode('ascii')
        email = user.email
        if isinstance(email, six.text_type):
            username = email.encode('utf-8')
        activation_key = hashlib.sha1(salt + email).hexdigest()
        return self.create(user=user,
                           activation_key=activation_key)

class RegistrationProfile(BaseRegistrationProfile):
    objects = RegistrationManager()

class AuthUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """ 
        Creates a saves a user with the given email 
        and password
        """

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates a saves a superuser with the given email
        and passworkd
        """

        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class LowerEmailField(models.EmailField):
    def to_python(self, value):
        value = super(LowerEmailField, self).to_python(value)
        if isinstance(value, basestring):
            return value.lower()
        return value

class AuthUser(AbstractBaseUser, PermissionsMixin):
    email = LowerEmailField(max_length=255, unique=True,)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    is_merchant = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=False)
    is_admin = models.BooleanField(default=False, null=False)

    # Sets custom AuthUser manager
    objects = AuthUserManager()

    # defines 'email' as identifier used for auth
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
        

    @property
    def username(self):
        """Fake username"""
        logger.debug('called fake "get" username')
        return self.email

    @username.setter
    def username(self, value):
        logger.debug('called fake "set" username')
        pass

    @username.deleter
    def username(self):
        logger.debug('called fake "delete" username')
        pass

    @classmethod
    def get_user_by_email(cls, email):
        """Looks up or or creates a new user if needed with specified email
        
        Returns tuple (is_existing, user)
        where is_existing True - user already existed, False - new user
        """
        
        user_model = get_user_model()
        try:
            existing_user = user_model.objects.get(email__iexact=email)
            if(existing_user):
                Profile.create_profile(existing_user)
                return (True, existing_user)
        except user_model.DoesNotExist:
            # this is ok, we will create a new user
            pass

        new_user = user_model.objects.create_user(email=email, password=None)
        new_user.first_name = ''
        new_user.last_name = ''
        new_user.is_merchant = False
        new_user.is_admin = False

        # Mark user as active. To actually use the account user has to
        # reset their password first. We will send them password reset
        # link along with their order or they can always
        # use 'forgot password' functionality to reset it
        new_user.is_active = True
        new_user.save()
        Profile.create_profile(new_user)
        return (False, new_user)

    @classmethod
    def compute_post_checkout_hash(cls, user):
        """Hashes email and user id
        
        Given any email address we can always lookup a user
        then using that user we can always compute this hash.
        This is useful if we want to perform a non-authenticated
        action when all we have is an email address
        """
        plain_text = "{0}|{1}".format(user.email, user.id)
        return hashlib.sha256(plain_text).hexdigest()

    def get_number_of_referrals(self):
        """Returns number of users who signed up using this user's referral link"""
        return self.user_join.all()[0].referral.all().count()

    def get_referral_link(self):
        result = settings.SHARE_URL
        result += self.user_join.all()[0].ref_id
        return result

    def get_number_of_reservations(self):
        return self.reservations.filter(is_active=True).count()

    def get_number_of_reservations_left(self):
        result = settings.RESERVATION_LIMIT - self.get_number_of_reservations()
        if(result < 0):
            result = 0
        return result

    def get_username_from_email(self):
        """Gets pre '@' portion of user's email"""
        try:
            handleindex = self.email.index(u'@')
            handle = self.email[:handleindex]
        except:
            handle = self.email
        return handle[:11]

    # Need to overide full_name and short_name from parent to make relevant
    def get_full_name(self):
        """ User is identified by their email """
        return self.email

    def get_short_name(self):
        """ User is identified by their email """
        return self.email

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if(self.email and self.email != self.email.lower()):
            self.email = self.email.lower()

        super(AuthUser, self).save(*args, **kwargs)
        useractivity = AuthUserActivity.objects.get_or_create(authuser=self)
        useractivity[0].save()

    @property
    def is_staff(self):
        """ Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def has_module_perms(self, app_label):
        if self.is_admin:
            if app_label == 'goods':
                return True
        return super(AuthUser, self).has_module_perms(app_label)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_admin:
            return True
        return super(AuthUser, self).has_perm(per, obj)


class Profile(models.Model):
    authuser = models.OneToOneField(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='profile')
    phone = PhoneNumberField(blank=True, null=False, default='')

    @classmethod
    def create_profile(cls, user):

        logger.debug("user id: [%s]" % str(user.id))

        profile = None
        try:
            profile = Profile.objects.get(authuser=user)
        except Profile.DoesNotExist:
            profile = Profile()
            profile.authuser = user
            profile.save()
        return profile


class PostalAddress(models.Model):
    street = models.CharField(max_length=50)
    street2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2, choices=States)
    zipcd = models.IntegerField()
    phone = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return ("{},{},{},{}".format(self.street, self.city, self.state, self.zipcd))

class AuthUserAddress(PostalAddress):
    authuser = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='default_address')


class AuthUserActivity(models.Model):
    authuser = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    # Items for which user has clicked on heart icon.
    saved_items = models.ManyToManyField('goods.Product', null=True, blank=True)
    # Items recommended by us to be associated with user
    recommended_items = models.ManyToManyField('goods.Product', related_name='recommended', null=True, blank=True)
    color = models.ManyToManyField('goods.Color', null=True, blank=True)
    style = models.ManyToManyField('goods.Style', null=True, blank=True)
    furnituretype = models.ManyToManyField('goods.FurnitureType', null=True, blank=True)
    value_tier = models.ManyToManyField('goods.ValueTier', null=True, blank=True)

    def __str__(self):
        return (self.authuser.email + ' UserActivityObject')

    class Meta:
        ordering = ['authuser']


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(blank=False, null=False)
    updated_at = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        """Sets/updates created_at and updated_at timestamps"""

        right_now = timezone.now()
        if(not self.id):
            self.created_at = right_now
        self.updated_at = right_now
        super(TimestampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class OrderType(object):
    """This class maintains a list of all order types
    similar to how OfferType has list of all the offer types
    """
    RESERVATION_ORDER = 'RESERVATION'
    PURCHASE_ORDER = 'PURCHASE'
    OFFER_ORDER = 'OFFER'

ORDER_TYPES = (
    (OrderType.RESERVATION_ORDER, 'Reservation'),
    (OrderType.PURCHASE_ORDER, 'Purchase'),
    (OrderType.OFFER_ORDER, 'Offer'),
)

class AuthOrder(TimestampedModel):
    authuser = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='user_orders')
    product = models.ForeignKey('goods.Product', blank=False, null=False, related_name='product_orders')
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, blank=False, null=False, db_index=True)
    converted_from_reservation = models.BooleanField(blank=False, null=False, default=False)

    def __unicode__(self):
        return u'user: {0}; item: {1}'.format(self.authuser.email, self.product.short_name)

    def reservation_conversion(self):
        """Converts reservation to purhcase order"""
        
        if(self.order_type == OrderType.PURCHASE_ORDER):
            # this is already a purchase, nothing else to do
            return
        
        if(self.order_type == OrderType.RESERVATION_ORDER and self.reservation):
            self.order_type = OrderType.PURCHASE_ORDER
            self.converted_from_reservation = True
            self.save()
            # TODO: create purchase from reservation
            
class OrderAddress(PostalAddress):
    order = models.OneToOneField(AuthOrder, related_name='address')

class Reservation(TimestampedModel):
    authuser = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='reservations')
    order = models.OneToOneField(AuthOrder, related_name='reservation')
    reservation_price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    reservation_expiration = models.DateTimeField(blank=False, null=False)

    @classmethod
    def create_reservation(cls, order):
        reservation = Reservation()
        reservation.authuser = order.authuser
        reservation.order = order
        reservation.reservation_price = order.product.current_price
        reservation.is_active = True
        reservation.reservation_expiration = timezone.now() + timedelta(hours=settings.RESERVATION_PERIOD)
        reservation.save()
        logger.debug('created Reservation')
        return reservation

    def cancel_reservation(self):
        self.is_active = False
        self.is_active = False
        self.save()

        product = self.order.product
        product.is_reserved = False
        product.save()


class PurchaseBase(TimestampedModel):
    authuser = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='%(class)s')
    taxes = models.DecimalField(max_digits=8, decimal_places=2, blank=None, null=None, default=0.00, help_text="Taxes in dollars")
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text='Price of the product at the time of purchase')
    transaction_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text='Total purchase price the user paid including promotions and taxes')

    @classmethod
    def compute_order_line_items(self, user, total_price_before_offers, promo_codes):
        offers = PromotionOffer.get_current_offers(user=user, promo_codes=promo_codes)

        discounts = []
        taxes = {}
        total = {}
        total_discount = 0

        # offers are available only to authenticated users
        if(user.is_authenticated()):
            for offer in offers:
                discount_dollar_value = offer.get_discount_dollar_value(total_price_before_offers=total_price_before_offers)
                if(discount_dollar_value):
                    discounts += [{
                                   'name': offer.name,
                                   'dollar_value': discount_dollar_value,
                                   'offer_id': offer.id,
                                   'promo_code': offer.code if offer.code in promo_codes else None
                                   }]
                    total_discount += discount_dollar_value
        subtotal_dollar_value = total_price_before_offers - total_discount
        taxes['dollar_value'] = subtotal_dollar_value * settings.SALES_TAX
        taxes['percentage'] = settings.SALES_TAX * 100

        total['in_dollars'] = Decimal(subtotal_dollar_value + taxes['dollar_value']).quantize(Decimal('.01'))
        total['in_cents'] = int(total['in_dollars'] * 100)

        return discounts, subtotal_dollar_value, taxes, total


    class Meta:
        abstract = True


class Purchase(PurchaseBase):

    order = models.OneToOneField(AuthOrder, related_name='purchase')

    @classmethod
    def create_purchase(cls, order, taxes, transaction_price):
        purchase = Purchase()
        purchase.authuser = order.authuser
        purchase.order = order
        purchase.taxes = taxes
        purchase.original_price = order.product.current_price
        purchase.transaction_price = transaction_price
        purchase.save()

        product = order.product
        product.is_sold = True
        product.is_reserved = False
        product.save()
        
        return purchase


class Offer(PurchaseBase):
    order = models.OneToOneField(AuthOrder, related_name='offer')
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text='Price offered by user')

    @classmethod
    def create_offer(cls, order, taxes, transaction_price, offer_price):
        offer = Offer()
        offer.authuser = order.authuser
        offer.order = order
        offer.taxes = taxes
        offer.original_price = order.product.current_price
        offer.transaction_price = transaction_price
        offer.offer_price = offer_price
        offer.save()

        product = order.product
        product.is_reserved = True
        product.save()

        return offer


class OfferType(object):
    """This class maintains a list of all Promotion Offer types
    
    Having this class allows us to use "constants" in our code.
    This is better because in case of a typo the compiler will catch it
    at compile time.
    
    To see the benefit consider these 2 cases:
    
    offers = PromotionOffer.objects.filter(offer_type = OfferType.FIRST_ORDERx)
    
    vs.
    
    offers = PromotionOffer.objects.filter(offer_type = 'FIRST_ORDERx')
    
    In both cases we made a typo notice extra "x", however in the first case
    compiler will catch this error as soon as we run the code, so we will be
    forced to fix it right away. In second case there is no compiler error 
    and we might never find the issue.
    """
    FIRST_ORDER = 'FIRST_ORDER'
    DISCOUNT_PROMO = 'DISCOUNT_PROMO'

OFFER_TYPES = (
    (OfferType.FIRST_ORDER, 'First order'),
    (OfferType.DISCOUNT_PROMO, 'Discount promo'),
)


class PromotionOffer(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, help_text='e.g. First order 10% off')
    short_terms = models.TextField(max_length=1000, blank=False, null=False, help_text='This is a short vertion of the terms that we can show to the user e.g. on a front page where they might actually read it.')
    terms = models.TextField(max_length=10000, blank=False, null=False, help_text='This is the "fine print", explaining in every details the terms of the promotion')
    limit_per_user = models.IntegerField(blank=False, null=False, help_text='Positive number - how many times this offer can be used per user, -1 - unlimited')

    # This takes precedence over any other fields when determining whether or not the offer is valid
    # e.g. start/end time or limit per user would only make sence if the offer is active
    # making default=False, so that we have to consiously enable it
    is_active = models.BooleanField(blank=False, null=False, default=False, help_text='This is On/Off switch for the offer')

    # we only have a one type for now, but there may be more
    # and each has to be handled differently
    # having a special field would allow us to figure out
    # how each 'kind' of offer should be handled
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPES, blank=False, null=False, db_index=True, help_text='This field determines how offer is applied: e.g. "First order", or "$10 off towards next purchase')

    start_time = models.DateTimeField(blank=True, null=True, default=None, help_text='When offer becomes available')
    end_time = models.DateTimeField(blank=True, null=True, default=None, help_text='When offer expires')
    is_code_required = models.BooleanField(blank=False, null=False, default=True)

    # codes must be unique, but they are also optional
    # we will handle the uniqueness in the 'save' method
    # because django can't handle unique and optinally empty fields
    # the way one would expect. I've ran into this long time ago,
    # but the issue still remains to this day see my stackoverflow question for details
    # http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
    code = models.CharField(max_length=100, blank=True, default='', db_index=True, help_text='Code for the promotion. Codes are case insensitive, e.g. PROMO2015 and Promo2015 is the same thing, so cannot create two different codes like that.')

    # For 'discount' kind of promotion either discount_fixed_amount or discount_percent must be set and be non-zero
    # we will handle this constraint in the save() method
    is_discount = models.BooleanField(blank=False, null=False, default=True, help_text='Is this offer containing a price discount? Some offer might not, e.g. Same day delivery is not a Discount kind of promition.')
    discount_fixed_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text='e.g. $20 off')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None, help_text='Expressed as percentage, e.g. 10 means 10% off')
    discount_limit = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text='Limits the Percent discount off to this value. This is applicable only when discount_percent is set')

    @classmethod
    def get_current_offers(cls, user=None, offer_type=None, promo_codes=None):
        """Returns all current offers

        if user is provided then filters out used up offers
        if promo_codes is provided then also includes specific offers for each promo code
        if offer_type is provided then only offers of this type will be considered, this takes precedence over promo_codes 
        """

        right_now = timezone.now()
        query = Q(is_code_required=False)
        if(promo_codes):
            query |= Q(is_code_required=True, code__in=promo_codes)

        offers = PromotionOffer.objects.filter(query, is_active=True, start_time__lte=right_now, end_time__gte=right_now)

        if(offer_type):
            offers = offers.filter(offer_type=offer_type)

        if(user):
            result = []
            for offer in offers:
                if(offer.limit_per_user == -1 or
                   offer.limit_per_user > Redemption.objects.filter(offer_id=offer.id, authuser_id=user.id).count()):
                    result += [offer]
            offers = result
        return offers

    @classmethod
    def is_valid_promo_code(cls, user, promo_code):
        """Checks if promo code is valid
        
        Does case insensitive comparison.
        If code is valid then returned promo_code would have proper capitalization
        
        Returns tuple (is_valid, promo_code, message)
        is_valid - boolean True - valid, False - invalid
        promo_code - if the code is valid this will 
            contain correct code with proper capitalization
            if code is not valid then this is same as the 
            input promo_code as-is
        message - if code is invalid this will contain a reason why
        
        Returning proper capitalizaion is needed so that we can later use it 
        when querying database using the "__in" query. Django does not support
        case insensitive filter using "__in"
        """

        # empty promo codes are invalid
        invalid_code_message = 'Invalid promo code'
        if(not promo_code):
            return (False, promo_code, invalid_code_message)

        right_now = timezone.now()
        proper_promo_code = None
        try:
            offer = PromotionOffer.objects.get(is_active=True,
                                               code__iexact=promo_code,
                                               start_time__lte=right_now,
                                               end_time__gte=right_now)
            proper_promo_code = offer.code
        except PromotionOffer.DoesNotExist:
            # did not find a valid offer for this promo code
            return (False, promo_code, invalid_code_message)

        # check whether the user used up all the offers
        

        if(user and
           offer.limit_per_user != -1 and
           offer.limit_per_user <= Redemption.objects.filter(offer_id=offer.id, authuser_id=user.id).count()):
            # no more such for this user
            return (False, promo_code, 'You have already used this promotion')
        elif not user.is_authenticated():
            return (False, promo_code, 'Please signup/login to use this promo')

        return (True, proper_promo_code, '')

    def get_discount_dollar_value(self, total_price_before_offers=None):
        if(self.is_discount):
            if(self.discount_fixed_amount and self.discount_fixed_amount <= total_price_before_offers):
                return self.discount_fixed_amount
            elif(self.discount_percent):
                discount = total_price_before_offers * self.discount_percent / 100
                if(self.discount_limit):
                    if(discount > self.discount_limit):
                        return self.discount_limit
                return discount
        return Decimal('0.0')

    def __unicode__(self):
        return u'%s (%s)' % (self.name, 'Active' if self.is_active else 'Inactive')

    def generate_code(self):
        """Returns a new unique code.
        
        When determining the uniqueness will do a case-insensitive check
        """

        CODE_LENGTH = 10
        random.seed()
        # Since we are generating the code randomly
        # so there is a chance the result might spell to
        # something offensive
        # To eliminate it we will not use any vowels or 0 (which looks like o) or 1 (which looks like i)
        alphabet = 'BCDFGHIGKLMNPQRSTVWXYZ23456789'
        while(True):

            result = ''
            for _i in xrange(CODE_LENGTH):
                result += random.choice(alphabet)
            if(PromotionOffer.objects.filter(code__iexact=result).count() == 0):
                # this is a unique code that does not exist yet
                # exactly what we need
                return result

    def save(self, *args, **kwargs):
        if(self.is_discount):
            if(not self.discount_fixed_amount and not self.discount_percent):
                raise Exception('Discount must be specified either as fixed amount or percent off, cannot have both values empty')
            if(self.discount_fixed_amount and self.discount_percent):
                raise Exception('Discount should be set either as a fixed amount or percent off but not both')
            if(self.discount_percent and (self.discount_percent > 100 or self.discount_percent < 0)):
                raise Exception('Discount percent can be between 0 and 100 inclusive')

        if(not self.id):  # this is a new order
            if(self.is_code_required and not self.code):
                self.code = self.generate_code()
        super(PromotionOffer, self).save(*args, **kwargs)


class Redemption(models.Model):
    authuser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_redemptions')
    offer = models.ForeignKey(PromotionOffer, blank=False, null=False, related_name='offer_redemptions')
    order = models.ForeignKey(AuthOrder, blank=False, null=False, related_name='order_redemptions')
    timestamp = models.DateTimeField(blank=False, null=False, help_text='When this was redeemed')

    total_before_discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text="Total dollar amount before applying any promotinal discounts to the order")
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text="Discount dollar amount")

    @classmethod
    def create_redemption(cls, order, product, offer_id, discount_dollar_value):
        redemption = Redemption()
        redemption.authuser = order.authuser
        redemption.offer_id = offer_id
        redemption.order = order
        redemption.timestamp = timezone.now()
        redemption.total_before_discount = product.current_price
        redemption.discount_amount = discount_dollar_value
        redemption.save()
        return redemption


class Join(models.Model):
    authuser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_join')
    friend = models.ForeignKey("self", related_name='referral', null=True, blank=True)
    ref_id = models.CharField(max_length=120, blank=False, null=False, unique=True)

    # client_id can be a GUID or an IP address - something that
    # helps us prevent multiple referrals from same real user
    client_id = models.CharField(max_length=120, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s" % (self.authuser.email)

    @classmethod
    def generate_ref_id(cls):
        ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
        try:
            if(Join.objects.get(ref_id=ref_id)):
                return cls.generate_ref_id()
        except Join.DoesNotExist:
            return ref_id

    @classmethod
    def create_join(cls, request, user):
        try:
            user_join = Join.objects.get(authuser__id=user.id)
            return user_join
        except Join.DoesNotExist:
            client_id = get_client_id(request)
            valid_referral = True
            if(Join.objects.filter(client_id=client_id).count() >= settings.LIMIT_REFERRAL_PER_CLIENT_ID):
                valid_referral = False
                logger.debug('reached the limit of referrals from the same client id')

            user_join = Join()
            user_join.authuser_id = user.id
            user_join.friend = None
            if(valid_referral):
                # count referrals only if not exceeding the limit from the same client id
                try:
                    join_id = request.session.get('join_id_ref', None)
                    user_join.friend = Join.objects.get(id=join_id) if join_id else None
                except Join.DoesNotExist:
                    pass
            user_join.ref_id = Join.generate_ref_id()
            user_join.client_id = client_id
            user_join.save()
            return user_join

# class AuthUserCart(models.Model):
#     authuser = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
#     saved_items = models.ManyToManyField('goods.Product')
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return ('Cart for user: ' + self.authuser.email + ';  items: ' + str(self.saved_items.all()))

#     def get_item_count(self):
#         return self.saved_items.all().count()

#     def get_cart_total(self):
#         total = 0
#         for product in self.saved_items.all():
#             total += product.current_price
#         return total

#     def get_cart_total_in_cents(self):
#         return int(self.get_cart_total() * 100)

#     def has_trial_products(self):
#         for product in self.saved_items.all():
#             if(product.has_trial):
#                 return True
#         return False
