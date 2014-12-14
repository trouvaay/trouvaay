from django.db import models
from djorm_pgarray.fields import IntegerArrayField
# Create your models here.
from helper import Attributes, AbstractImageModel


class Segment(models.Model):
	description = models.CharField(max_length=50, choices=Attributes['segment'])
	
	def __str__(self):
		return self.description

class Style(models.Model):
	description = models.CharField(max_length=50, choices=Attributes['style'])

	def __str__(self):
		return self.description

class Category(models.Model):
	description = models.CharField(max_length=50, choices=Attributes['category'])

	def __str__(self):
		return self.description

class Subcategory(models.Model):
	description = models.CharField(max_length=50, choices=Attributes['subcategory'])

	def __str__(self):
		return self.description

class Material(models.Model):
	description = models.CharField(max_length=50, choices=Attributes['material'])	

	def __str__(self):
		return self.description

class Product(models.Model):
	sku = models.CharField(max_length=25, null=True, blank=True)
	long_name = models.CharField(max_length=50, null=True, blank=True)
	short_name = models.CharField(max_length=25)
	original_price = models.IntegerField()
	current_price = models.IntegerField()
	store = models.ForeignKey('merchants.Store')
	manufacturer = models.CharField(max_length=25, null=True, blank=True)
	units = models.IntegerField(default=1)
	care = models.TextField(null=True, blank=True)
	dimensions = IntegerArrayField(dimension=3)
	weight = models.IntegerField(null=True, blank=True)
	return_policy = models.TextField(null=True, blank=True)
	color = models.CharField(max_length=20, null=True, blank=True)
	segment = models.ManyToManyField(Segment, null=True, blank=True)
	style = models.ManyToManyField(Style, null=True, blank=True, verbose_name='style')
	category = models.ManyToManyField(Category, null=True, blank=True)
	subcategory = models.ManyToManyField(Subcategory, null=True, blank=True)
	material = models.ManyToManyField(Material, null=True, blank=True)
	added_date = models.DateTimeField(auto_now_add=True)
	pub_date = models.DateTimeField()
	is_published = models.BooleanField(default=True)

	def __str__(self):
		return self.short_name

class ProductImage(AbstractImageModel):
	product = models.ForeignKey('goods.Product')

	class Meta:
		app_label = 'goods'

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
	Message = models.CharField(max_length=255)
	added_date = models.DateTimeField(auto_now_add=True)
	last_comm_date = models.DateTimeField(auto_now=True)
	is_published = models.BooleanField(default=True)
	pub_date = models.DateTimeField()




