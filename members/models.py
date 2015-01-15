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
		return ("{},{},{},{},{}".format(self.street,self.city,self.state,self.zipcd))

class AuthUserActivity(models.Model):
	authuser = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
	# Items for which user has clicked on heart icon.
	saved_items = models.ManyToManyField('goods.Product', null=True, blank=True)
	# Items recommended by us to be associated with user
	recommended_items = models.ManyToManyField('goods.Product', related_name='recommended')
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



