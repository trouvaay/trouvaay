from localflavor.us.models import (
	PhoneNumberField,
	USStateField,
	)

from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin,
	BaseUserManager
	)
from django.db import models
from django.conf import settings
from helper import States
from registration.models import RegistrationManager as BaseRegistrationManager
from registration.models import RegistrationProfile as BaseRegistrationProfile
from django.contrib.auth import get_user_model
import hashlib
import six
import random

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
		activation_key = hashlib.sha1(salt+email).hexdigest()
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

		user = self.create_user(email,password=password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True,)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)
	is_merchant = models.BooleanField(default=False)
	date_joined = models.DateTimeField(auto_now_add=True)
	in_coverage_area = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True, null=False)
	is_admin = models.BooleanField(default=False, null=False)

	# Sets custom AuthUser manager
	objects = AuthUserManager()

	#defines 'email' as identifier used for auth
	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = []

	#Need to overide full_name and short_name from parent to make relevant
	def get_full_name(self):
		""" User is identified by their email """
		return self.email

	def get_short_name(self):
		""" User is identified by their email """
		return self.email

	def __str__(self):
		return self.email

	def save(self, *args, **kwargs):
		super(AuthUser, self).save(*args, **kwargs)
		useractivity = AuthUserActivity.objects.get_or_create(authuser=self)
		useractivity[0].save()
	
	@property
	def is_staff(self):
		""" Is the user a member of staff?"""
		# Simplest possible answer: All admins are staff
		return self.is_admin

class AuthUserAddress(models.Model):
	authuser = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
	street = models.CharField(max_length=50)
	street2 = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=20)
	state = models.CharField(max_length=2, choices=States)
	zipcd = models.IntegerField()
	phone =  models.CharField(max_length=120)
	shipping = models.BooleanField(default=True)
	billing = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	lat = models.FloatField(null=True, blank=True)
	lng = models.FloatField(null=True, blank=True)

	def __str__(self):
		return ("{},{},{},{}".format(self.street,self.city,self.state,self.zipcd))

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
		return ('user: '+self.authuser.email+' ;  items: '+str(self.saved_items.all()))

	class Meta:
		ordering = ['authuser']

# class AuthUserDesiredObject(models.Model):
# 	fur

class AuthUserStripe(models.Model):
	authuser = models.OneToOneField(settings.AUTH_USER_MODEL)
	stripe_id = models.CharField(max_length=120, null=True, blank=True)

	def __unicode__(self):
		return str(self.stripe_id)

class AuthUserCart(models.Model):
	authuser = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
	saved_items = models.ManyToManyField('goods.Product')
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return ('Cart for user: '+self.authuser.email+';  items: '+str(self.saved_items.all()))
	
	def get_item_count(self):
		return self.saved_items.all().count()

	def get_cart_total(self):
		total = 0
		for product in self.saved_items.all():
			total+=product.current_price
		return total

	def get_cart_total_in_cents(self):
		return int(self.get_cart_total() * 100)

	def has_trial_products(self):
		for product in self.saved_items.all():
			if(product.has_trial):
				return True
		return False


class AuthUserOrder(models.Model):
	"""Unique User-Order pair"""
	authuser = models.ForeignKey(settings.AUTH_USER_MODEL)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def get_captured_amt(self):
		"""some of total amount captured on current transaction
		"""
		total = 0
		for ordered_item in self.authuserorderitem_set.filter(captured=True):
			total+=ordered_item.sell_price
		return total

	def get_item_count(self):
		return self.authuserorderitem_set.all().count()

	def get_order_total(self):
		total = 0
		for ordered_item in self.authuserorderitem_set.all():
			total+=ordered_item.sell_price
		return total

	def __str__(self):
		return('user: '+self.authuser.email+' ;  items: '+str(self.authuserorderitem_set.all()))

class AuthUserOrderItem(models.Model):
	"""Unique product-order pair"""

	product = models.ForeignKey('goods.Product')
	order = models.ForeignKey(AuthUserOrder, null=True, blank=True)
	sell_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	captured = models.BooleanField(default=True)
	#for buy-and-trial items, time at which transaction will be captured
	capture_time = models.DateTimeField(null=True, blank=True)

	#for now we only have purchase quantities of one but in the future will allow
	#for purchase of multiple of same item
	quantity = models.IntegerField(default=1)
	






