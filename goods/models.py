from django.db import models
from helper import AbstractImageModel
from math import acos, cos, radians, sin
from django.utils import timezone


class Segment(models.Model):
	select = models.CharField(max_length=55, default='new', null=True, blank=True)	
	def __str__(self):
		return self.select or 'none'

class Style(models.Model):
	select = models.CharField(max_length=55, default='modern', null=True, blank=True)	
	def __str__(self):
		return self.select or 'none'

class FurnitureType(models.Model):
	select = models.CharField(max_length=55, default='seating', null=True, blank=True)	
	def __str__(self):
		return self.select or 'none'

class ValueTier(models.Model):
	select = models.CharField(max_length=55, default='mid', null=True, blank=True)	
	def __str__(self):
		return self.select or 'none'

class Category(models.Model):
	select = models.CharField(max_length=55, default='living', null=True, blank=True)	
	def __str__(self):
		return self.select or 'none'

class Subcategory(models.Model):
	select = models.CharField(max_length=55, default='bar', null=True, blank=True)
	trial_product = models.BooleanField(default=False)	
	def __str__(self):
		return self.select or 'none'

class Color(models.Model):
	select = models.CharField(max_length=55, default='blue', null=True, blank=True)	
	def __str__(self):
		return self.select or 'none'

class Material(models.Model):
	select = models.CharField(max_length=55, default='leather', null=True, blank=True)	
	def __str__(self):
		return self.select or 'none'

# subcategories = [
# 		('bar', 'bar'),
# 		('bar_stool','bar_stool'),
# 		('bed','bed'),
# 		('bedding','bedding'),
# 		('bench','bench'),
# 		('chair','chair'),
# 		('chaise','chaise'),
# 		('desk','desk'),
# 		('desk_light','desk_light'),
# 		('dining_table','dining_table'),
# 		('dresser', 'dresser'),
# 		('floor_lamp','floor_lamp'),
# 		('kitchen_serving','kitchen_serving'),
# 		('lighting - other', 'lighting - other'),
# 		('loveseat','loveseat'),
# 		('media','media'),
# 		('mirror','mirror'),
# 		('ottoman','ottoman'),
# 		('other_lighting','other_lighting'),
# 		('other_decor ','other_decor '),
# 		('pillow','pillow'),
# 		('rug_throw','rug_throw'),
# 		('table_lamp', 'table_lamp', )
# 		('small_table','small_table'),
# 		('sofa','sofa'),
# 		('storage','storage'),
# 		('wall_decor','wall_decor'),
# 	]


class Product(models.Model):
	sku = models.CharField(max_length=25, null=True, blank=True)
	short_name = models.CharField(max_length=50)
	original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	current_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	value_tier = models.ForeignKey(ValueTier, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	store = models.ForeignKey('merchants.Store')
	manufacturer = models.CharField(max_length=25, null=True, blank=True)
	units = models.IntegerField(default=1)
	care = models.TextField(null=True, blank=True)
	width = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	depth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	seat_height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	diameter = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	bed_size = models.CharField(max_length=50, null=True, blank=True)
	weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
	return_policy = models.TextField(null=True, blank=True)
	color = models.ManyToManyField(Color, null=True, blank=True)
	color_description = models.CharField(max_length=100, null=True, blank=True)
	segment = models.ManyToManyField(Segment, null=True, blank=True)
	style = models.ManyToManyField(Style, null=True, blank=True, verbose_name='style')
	furnituretype = models.ManyToManyField(FurnitureType, null=True, blank=True)
	category = models.ManyToManyField(Category, null=True, blank=True)
	subcategory = models.ManyToManyField(Subcategory, null=True, blank=True)
	material = models.ManyToManyField(Material, null=True, blank=True)
	added_date = models.DateTimeField(auto_now_add=True)
	pub_date = models.DateTimeField()
	has_trial = models.BooleanField(default=False)
	is_sold = models.BooleanField(default=False)
	is_published = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=False)
	lat = models.FloatField(null=True, blank=True)
	lng = models.FloatField(null=True, blank=True)

	class Meta:
		ordering = ['-pub_date']

	def __str__(self):
		return self.short_name

	def save(self, *args, **kwargs):
		self.lat = self.store.lat
		self.lng = self.store.lng
		if self.is_published == True and not self.pub_date:
			self.pub_date = timezone.now()
		super(Product, self).save(*args, **kwargs)
		self.does_product_have_trial()


	def getdist(self, UserLat=39.94106319,UserLng=-75.173192):
		dist = 3959 * acos(cos(radians(UserLat)) * cos(radians(self.lat)) \
		* cos(radians(self.lng) - radians(UserLng)) + sin(radians(UserLat))*\
		sin(radians(self.lat)))      
    	
		return round(dist,2)

	def does_product_have_trial(self):
		"""if product is part of a subcategory that
		is triable OR has a price above $1000, it is eligible for a trial
		"""

		trial_list = Subcategory.objects.filter(trial_product=True)
		if self.current_price > 1000 or self.subcategory in trial_list:
			self.has_trial = True

class ProductImage(AbstractImageModel):
	product = models.ForeignKey('goods.Product')

	class Meta:
		app_label = 'goods'

	def __str__(self):
		return self.product.short_name

class ProductActivity(models.Model):
	product = models.ForeignKey(Product)
	likes = models.IntegerField(default=0)
	shares = models.IntegerField(default=0)
	views = models.IntegerField(default=0)

	class Meta:
		abstract = True

class NewProductActivity(ProductActivity):
	units_sold = models.IntegerField(default=0)

class VintageProductActivity(ProductActivity):
	time_to_sale = models.IntegerField(default=0)

class Comment(models.Model):
	product = models.ForeignKey(Product)
	authuser = models.ForeignKey('members.AuthUser')
	message = models.CharField(max_length=255)
	added_date = models.DateTimeField(auto_now_add=True)
	is_published = models.BooleanField(default=True)
	pub_date = models.DateTimeField(null=True, blank=True)

	def days_since_add(self):
		delta = timezone.now() - self.added_date
		time_lapse = delta.days

		return int(time_lapse)




