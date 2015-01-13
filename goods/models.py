from django.db import models
from helper import AbstractImageModel
from math import acos, cos, radians, sin
from django.utils import timezone


class Segmentmodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='new', null=True, blank=True)	
	def __str__self):
		return self.select or 'none'

	class Meta:
		ordering = ['select']

class Stylemodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='modern', null=True, blank=True)	
	def __str__self):
		return self.select or 'none'

	class Meta:
		ordering = ['select']

class FurnitureTypemodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='seating', null=True, blank=True)	
	def __str__self):
		return self.select or 'none'

	class Meta:
		ordering = ['select']

class ValueTiermodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='mid', null=True, blank=True)	
	def __str__self):
		return self.select or 'none'

	class Meta:
		ordering = ['select']

class Categorymodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='living', null=True, blank=True)	
	def __str__self):
		return self.select or 'none'

	class Meta:
		ordering = ['select']

class Subcategorymodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='bar', null=True, blank=True)
	trial_product = models.BooleanFielddefault=False)	
	def __str__self):
		return self.select or 'none'

	class Meta:
		ordering = ['select']

class Colormodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='blue', null=True, blank=True)	
	def __str__self):
		return self.select or 'none'
	
	class Meta:
		ordering = ['select']

class Materialmodels.Model):
	select = models.CharFieldunique=True, max_length=55, default='leather', null=True, blank=True)	
	def __str__self):
		return self.select or 'none'
	
	class Meta:
		ordering = ['select']

subcategories = {
		'armoire': [100, 200, 400],
		'bar': [100, 200, 400],
		'bar stool':[100, 200, 400],
		'bed':[100, 200, 400],
		'bedding':[100, 200, 400],
		'bench':[100, 200, 400],
		'cabinet':[100, 200, 400],
		'chair - accent':[100, 200, 400],
		'chair - dining':[100, 200, 400],
		'chaise':[100, 200, 400],
		'decor - wall':[100, 200, 400],
		'decor - table':[100, 200, 400],
		'decor - other':[100, 200, 400],
		'desk':[100, 200, 400],
		'desk light':[100, 200, 400],
		'dining table':[100, 200, 400],
		'dresser':[100, 200, 400],
		'kitchen and serving':[100, 200, 400],
		'lighting - floor':[100, 200, 400],
		'lighting - desk':[100, 200, 400],
		'lighting - other':[100, 200, 400],
		'loveseat':[100, 200, 400],
		'media','media'),
		'mirror','mirror'),
		'ottoman','ottoman'),
		'pillow','pillow'),
		'rug','rug'),
		'sofa','sofa'),
		'storage','storage'),
		'table - large','table - large'),
		'table - small','table - small'),
		'throw', 'throw'),
		'trunk', 'trunk'),
		'table', 'table'),
	]


class Productmodels.Model):
	sku = models.CharFieldmax_length=25, null=True, blank=True)
	short_name = models.CharFieldmax_length=50)
	original_price = models.DecimalFieldmax_digits=8, decimal_places=2, default=0.00)
	current_price = models.DecimalFieldmax_digits=8, decimal_places=2, default=0.00)
	value_tier = models.ForeignKeyValueTier, null=True, blank=True)
	description = models.TextFieldnull=True, blank=True)
	store = models.ForeignKey'merchants.Store')
	manufacturer = models.CharFieldmax_length=25, null=True, blank=True)
	units = models.IntegerFielddefault=1)
	care = models.TextFieldnull=True, blank=True)
	width = models.DecimalFieldmax_digits=6, decimal_places=2, null=True, blank=True)
	depth = models.DecimalFieldmax_digits=6, decimal_places=2, null=True, blank=True)
	height = models.DecimalFieldmax_digits=6, decimal_places=2, null=True, blank=True)
	seat_height = models.DecimalFieldmax_digits=6, decimal_places=2, null=True, blank=True)
	diameter = models.DecimalFieldmax_digits=6, decimal_places=2, null=True, blank=True)
	bed_size = models.CharFieldmax_length=50, null=True, blank=True)
	weight = models.DecimalFieldmax_digits=5, decimal_places=1, null=True, blank=True)
	return_policy = models.TextFieldnull=True, blank=True)
	color = models.ManyToManyFieldColor, null=True, blank=True)
	color_description = models.CharFieldmax_length=100, null=True, blank=True)
	segment = models.ManyToManyFieldSegment, null=True, blank=True)
	style = models.ManyToManyFieldStyle, null=True, blank=True, verbose_name='style')
	furnituretype = models.ManyToManyFieldFurnitureType, null=True, blank=True)
	category = models.ManyToManyFieldCategory, null=True, blank=True)
	subcategory = models.ManyToManyFieldSubcategory, null=True, blank=True)
	material = models.ManyToManyFieldMaterial, null=True, blank=True)
	added_date = models.DateTimeFieldauto_now_add=True)
	pub_date = models.DateTimeField)
	has_trial = models.BooleanFielddefault=False)
	is_sold = models.BooleanFielddefault=False)
	is_published = models.BooleanFielddefault=True)
	is_featured = models.BooleanFielddefault=False)
	lat = models.FloatFieldnull=True, blank=True)
	lng = models.FloatFieldnull=True, blank=True)

	class Meta:
		ordering = ['-pub_date']

	def __str__self):
		return self.short_name

	def saveself, *args, **kwargs):
		self.lat = self.store.lat
		self.lng = self.store.lng
		if self.is_published == True and not self.pub_date:
			self.pub_date = timezone.now)
		superProduct, self).save*args, **kwargs)
		self.does_product_have_trial)


	def getdistself, UserLat=39.94106319,UserLng=-75.173192):
		dist = 3959 * acoscosradiansUserLat)) * cosradiansself.lat)) \
		* cosradiansself.lng) - radiansUserLng)) + sinradiansUserLat))*\
		sinradiansself.lat)))      
    	
		return rounddist,2)

	def does_product_have_trialself):
		"""if product is part of a subcategory that
		is triable OR has a price above $1000, it is eligible for a trial
		"""

		trial_list = Subcategory.objects.filtertrial_product=True)
		if self.current_price >= 1000 or self.subcategory.first) in trial_list:
			self.has_trial = True

class ProductImageAbstractImageModel):
	product = models.ForeignKey'goods.Product')

	class Meta:
		app_label = 'goods'

	def __str__self):
		return self.product.short_name


#FUTURE FEATURES
# class ProductActivitymodels.Model):
# 	product = models.ForeignKeyProduct)
# 	likes = models.IntegerFielddefault=0)
# 	shares = models.IntegerFielddefault=0)
# 	views = models.IntegerFielddefault=0)

# 	class Meta:
# 		abstract = True

# class NewProductActivityProductActivity):
# 	units_sold = models.IntegerFielddefault=0)
# class VintageProductActivityProductActivity):
# 	time_to_sale = models.IntegerFielddefault=0)

# class Commentmodels.Model):
# 	product = models.ForeignKeyProduct)
# 	authuser = models.ForeignKey'members.AuthUser')
# 	message = models.CharFieldmax_length=255)
# 	added_date = models.DateTimeFieldauto_now_add=True)
# 	is_published = models.BooleanFielddefault=True)
# 	pub_date = models.DateTimeFieldnull=True, blank=True)

# 	def days_since_addself):
# 		delta = timezone.now) - self.added_date
# 		time_lapse = delta.days

# 		return inttime_lapse)




