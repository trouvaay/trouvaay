from django.db import models
from helper import AbstractImageModel
from django.utils import timezone
from django.db.models.signals import post_save, m2m_changed
from django.core.urlresolvers import reverse
import itertools
import hashlib
import requests
import cloudinary
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify
from django.db.models import F
from django.utils.encoding import smart_text
from django.conf import settings
from decimal import Decimal
from members.models import PromotionOffer
import logging
from datetime import timedelta
import math

logger = logging.getLogger(__name__)


class Segment(models.Model):
    select = models.CharField(unique=True, max_length=55, default='new', null=True, blank=True)

    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']


class Style(models.Model):
    select = models.CharField(unique=True, max_length=55, default='modern', null=True, blank=True)

    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']


class FurnitureType(models.Model):
    select = models.CharField(unique=True, max_length=55, default='seating', null=True, blank=True)
    is_furniture = models.BooleanField(default=True)

    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']


class ValueTier(models.Model):
    select = models.CharField(unique=True, max_length=55, default='mid', null=True, blank=True)

    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']


class Category(models.Model):
    select = models.CharField(unique=True, max_length=55, default='living', null=True, blank=True)

    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']


class Subcategory(models.Model):
    select = models.CharField(unique=True, max_length=55, default='bar', null=True, blank=True)
    trial_product = models.BooleanField(default=False)
    shipping_charge = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, choices=[(5.00, 5.00), (20.00, 20.00), (50.00, 50.00)])

    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']


class Color(models.Model):
    select = models.CharField(unique=True, max_length=55, default='blue', null=True, blank=True)

    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']


class Material(models.Model):
    select = models.CharField(unique=True, max_length=55, default='leather', null=True, blank=True)
    def __str__(self):
        return self.select or 'none'

    class Meta:
        ordering = ['select']

def add_img_instance(product_pk, img_url, is_main=False):
    upload_response = cloudinary.uploader.upload(img_url)
    cloudinary_image = cloudinary.CloudinaryImage(metadata=upload_response)
    product = Product.objects.get(pk=product_pk)
    product_image = ProductImage()
    product_image.image = cloudinary_image
    product_image.is_main = is_main
    product_image.product = product
    product_image.save()
    

class Product(models.Model):
    sku = models.CharField(max_length=25, null=True, blank=True)
    short_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=255)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    description = models.TextField(null=True, blank=True)
    store = models.ForeignKey('merchants.Store')
    manufacturer = models.CharField(max_length=25, null=True, blank=True)
    units = models.IntegerField(default=1)
    url = models.URLField(null=True, blank=True, max_length=255)
    minimum_offer_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=None)

    # Dimensions & Attributes
    width = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    seat_height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    diameter = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    bed_size = models.CharField(max_length=50, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    color = models.ManyToManyField(Color, null=True, blank=True)
    color_description = models.CharField(max_length=100, null=True, blank=True)
    material = models.ManyToManyField(Material, null=True, blank=True)
    material_description = models.CharField(max_length=255, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)  # list of tag words
    is_custom = models.BooleanField(default=False)
    is_floor_model = models.BooleanField(default=False)

    # Categorization
    segment = models.ManyToManyField(Segment, null=True, blank=True)
    style = models.ManyToManyField(Style, null=True, blank=True, verbose_name='style')
    furnituretype = models.ManyToManyField(FurnitureType, null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    subcategory = models.ManyToManyField(Subcategory, null=True, blank=True)  # required for has_trial

    # Availability
    added_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_recent = models.BooleanField(default=True)
    hours_left = models.IntegerField(default=settings.SHELF_LIFE, null=True, blank=True)
    is_landing = models.BooleanField(default=False)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    md5_order = models.CharField(max_length=32, null=True, blank=True)
    click_count = models.IntegerField(blank=False, null=False, default=0)
    display_score = models.IntegerField(blank=False, null=False, default=0)
    the_hunt = models.BooleanField(default=False)

    class Meta:
        ordering = ['-display_score', 'md5_order']
        unique_together = ('short_name', 'store',)

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        # return self.slug
        return reverse('goods:detail', args=[self.slug])

    def calc_display_score(self):
        score = 0

        # get price score
        price_score = 0
        if self.current_price < 200.00:
            price_score = 8
        elif self.current_price < 400.00:
            price_score = 5
        elif self.current_price < 500.00:
            price_score = 3
        
        print('price score = ', price_score)  
        score+=price_score
        print('current score: ', score)
        
        # get date added score
        pub_dt_score = 0
        try:
            days_left = self.hours_to_delist()/24.0
            if days_left:
                if days_left > 29:
                    pub_dt_score = 20
                elif days_left > 25:
                    pub_dt_score = 10
                elif days_left > 20:
                    pub_dt_score = 5
                elif days_left > 15:
                    pub_dt_score = 3
        except:
            pass

        print('pub_dt_score = ', pub_dt_score)
        score+=pub_dt_score
        print('current score: ', score)
        
        # get category score
        category_score = 0
        if self.furnituretype.all() and self.furnituretype.all()[0].select in ['seating', 'tables']:
            category_score = 3

        print('cat_score = ', category_score)
        score+=category_score
        print('current score: ', score)

        #is_available score
        available_score = 0
        if self.is_reserved:
            available_score = -3
        elif self.is_sold:
            available_score = -5

        print('avail_score = ', available_score)
        score+=available_score
        print('current score: ', score)

        #add click count
        click_score = 0
        if self.click_count > 20:
            click_score = 8
        elif self.click_count > 10:
            click_score = 4
        elif self.click_count > 5:
            click_score = 2
        
        score+=click_score
        print('click count = ', self.click_count)
        
        print(' final score = ', score)
        
        self.display_score = score
        self.save()

    def save(self, *args, **kwargs):
        self.lat = self.store.lat
        self.lng = self.store.lng

        # Check to see if pub date is missing if item is published.
        if self.is_published:
            if (not self.pub_date):
                self.pub_date = timezone.now()
        
        # if item is not published, pub_date should be blank
        elif (not self.is_published):
            self.pub_date = None
            self.hours_left = None
        # Update is_recent Field
        else:
            if((self.pub_date <= (timezone.now() - timedelta(hours=settings.RECENT_PRODUCT_AGE))) and self.is_recent):
                self.is_recent = False

            elif((self.pub_date > (timezone.now() - timedelta(hours=settings.RECENT_PRODUCT_AGE))) and (not self.is_recent)):
                self.is_recent = True

        #Update minimumim_offer_price field
        self.minimum_offer_price = self.current_price * settings.OFFER_THRESHOLD

        # create slug once, only if we don't have it yet
        if(not self.slug):
            self.slug = slugify(self.short_name)
            for x in itertools.count(1):
                if not Product.objects.filter(slug=self.slug).exists():
                    break
                # append number to slug if it already exists
                self.slug = '%s-%d' % (self.slug, x)

        # Create has for unique value for product sorting
        self.add_md5_order()
        super(Product, self).save(*args, **kwargs)
            
    def add_md5_order(self):
        u = hashlib.md5()
        u.update(self.slug)
        self.md5_order = u.hexdigest()

    def is_discounted(self):
        return (self.current_price < self.original_price)

    def get_price_in_cents(self):
        return int(self.current_price * 100)

    def get_price_in_cents_with_tax(self):
        return int(self.get_price_in_cents() * (1 + settings.SALES_TAX))

    def get_price_in_cents_for_checkout(self):
        """Computes final price for checkout by applying taxes and all discounts"""
        pass
#
#         total_in_dollars = Decimal(self.get_price_in_cents_with_tax() / 100)
#         discounts_in_dollars = 0
#         offers = PromotionOffer.objects.
#             # get offers from
#         for offer in offers:
#             discounts_in_dollars += offer.get_offer_discount(total_in_dollars)
#         return int((total_in_dollars - discounts_in_dollars) * 100)

    def hours_since_add(self):
        if self.pub_date:
            delta = timezone.now() - self.pub_date
            time_lapse = delta.total_seconds() // 3600
            return int(time_lapse)
        else:
            return None

    def hours_to_delist(self):
        if self.is_published:
            delist_date =  self.pub_date + timedelta(seconds=settings.SHELF_LIFE*3600)
            delta = delist_date - timezone.now()
            time_lapse = delta.total_seconds() // 3600
            return int(time_lapse)

    def get_days_left(self):
        if self.hours_left / 24.0 > 1:
            return ('{} days left'.format(int(math.ceil(self.hours_left / 24.0))))
        else:
            return 'last day'


    def has_returns(self):
        return self.store.has_returns


    def is_furniture(self):
        """ Test whether furnituretypes have furniture set to True """
        furniture = [str(i) for i in FurnitureType.objects.filter(is_furniture=True)]
        if [i for i in self.furnituretype.all() if i.select in furniture]:
            return True
        else:
            return False

    def has_dimensions(self):
        """Checks to see if any of dimension fields are not null/blank
        """
        dimensions = [self.width, self.height, self.depth]
        if all(dimen is None for dimen in dimensions):
            return False
        else:
            return True

    def get_dimension(self, dimension):
        """ Appends '"Wx to approapriate dimension for 
        template rendering.  Ie 10 --> 10"W
        """
        try:
            value = round(getattr(self, dimension), 1)
            appendterm = dimension[0].upper()
            return (str(value) + '"' + appendterm)
        except:
            pass


    def get_dimension_str(self):
        dimension_list = ['width', 'height', 'depth']
        dimension_str = ""
        for dimension in dimension_list:
            if self.get_dimension(dimension):
                dimension_str += (self.get_dimension(dimension) + ' x ')
        return dimension_str[:-3]

    @property
    def is_vintage(self):
        if len(self.segment.filter(select__icontains="vintage")):
            return True
        else:
            return False


class ProductImage(AbstractImageModel):
    product = models.ForeignKey('goods.Product')

    class Meta:
        app_label = 'goods'
        ordering = ['-is_main']

    def __str__(self):
        return self.product.short_name


# FUTURE FEATURES
# class ProductActivity(models.Model):
#   product = models.ForeignKey(Product)
#   likes = models.IntegerField(default=0)
#   shares = models.IntegerField(default=0)
#   views = models.IntegerField(default=0)

#   class Meta:
#       abstract = True

# class NewProductActivity(ProductActivity):
#   units_sold = models.IntegerField(default=0)
# class VintageProductActivity(ProductActivity):
#   time_to_sale = models.IntegerField(default=0)

# class Comment(models.Model):
#   product = models.ForeignKey(Product)
#   authuser = models.ForeignKey('members.AuthUser')
#   message = models.CharField(max_length=255)
#   added_date = models.DateTimeField(auto_now_add=True)
#   is_published = models.BooleanField(default=True)
#   pub_date = models.DateTimeField(null=True, blank=True)

#   def days_since_add(self):
#       delta = timezone.now() - self.added_date
#       time_lapse = delta.days

#       return int(time_lapse)
# subcategories = {
#       'armoire': [100, 200, 400],
#       'bar'
#       'bar stool'
#       'bed'
#       'bedding'
#       'bench':
#       'cabinet':
#       'chair - accent':
#       'chair - dining':
#       'chaise':
#       'decor - wall','decor - wall'),
#       'decor - table','decor - table'),
#       'decor - other','decor - other'),
#       ('desk','desk'),
#       ('desk light','desk light'),
#       ('dining table','dining table'),
#       ('dresser', 'dresser'),
#       ('kitchen and serving','kitchen and serving'),
#       ('lighting - floor','lighting - floor'),
#       ('lighting - desk', 'lighting - desk'),
#       ('lighting - other', 'lighting - other'),
#       ('loveseat','loveseat'),
#       ('media','media'),
#       ('mirror','mirror'),
#       ('ottoman','ottoman'),
#       ('pillow','pillow'),
#       ('rug','rug'),
#       ('sofa','sofa'),
#       ('storage','storage'),
#       ('table - large','table - large'),
#       ('table - small','table - small'),
#       ('throw', 'throw'),
#       ('trunk', 'trunk'),
#       ('table', 'table'),
#   ]




