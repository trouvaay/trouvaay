from localflavor.us.models import PhoneNumberField
from django.db import models
from django.conf import settings
from helper import States, GeoCode, AbstractImageModel


class Retailer(models.Model):
	legal_name = models.CharField(max_length=255)
	short_name = models.CharField(max_length=100)
	organization_type = models.CharField(max_length=20, choices=[('indiv','individual'),('corp.','corporation')])
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_merchant': True})
	website = models.URLField(null=True, blank=True)

	def __str__(self):
		return self.short_name

class RetailerImage(AbstractImageModel):
	retailer = models.ForeignKey('merchants.Retailer')
	is_logo = models.BooleanField(default=False)

	class Meta:
		app_label = 'merchants'

	def __str__(self):
		return self.retailer.short_name

class Shipper(models.Model):
	name = models.CharField(max_length=100, unique=True)
	phone = PhoneNumberField(max_length=12)
	email = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.name

class Store(models.Model):
	retailer = models.ForeignKey(Retailer)
	store_num = models.CharField(max_length=10,null=True, blank=True)
	street = models.CharField(max_length=50)
	street2 = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=20)
	state = models.CharField(max_length=2, choices=States)
	zipcd = models.IntegerField()
	lat = models.FloatField(null=True, blank=True)
	lng = models.FloatField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	shipper = models.ManyToManyField(Shipper, null=True, blank=True)
	is_featured = models.BooleanField(default=False)

	class Meta:
		ordering = ['retailer', 'street']

	def __str__(self):
		return (self.retailer.short_name+" ("+self.street[:12]+")")
	
	def _geo_code(self):
		print( GeoCode(self.street,self.city,
						self.state, self.zipcd,self.street2))

	def save(self, *args, **kwargs):
		#updates lat/lng when saved
		#TODO: update so lat/lng only updated when needed
		# self.lat, self.lng = self._geo_code()
		super(Store, self).save(*args, **kwargs)	