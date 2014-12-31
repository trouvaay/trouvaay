from localflavor.us.models import (
	PhoneNumberField,
	USStateField,
	)

from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin,
	BaseUserManager
	)
from django.db import models
from helper import Attributes



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

	@property
	def is_staff(self):
		""" Is the user a member of staff?"""
		# Simplest possible answer: All admins are staff
		return self.is_admin


class AuthUserActivity(models.Model):
	authuser = models.ForeignKey(AuthUser)
	saved_items = models.ManyToManyField('goods.Product')
	style = models.ManyToManyField('goods.Style') #need to add other attrs

	def __str__(self):
		return ('user: '+self.authuser.email+' ;  items: ')
