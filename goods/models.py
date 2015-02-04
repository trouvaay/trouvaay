from django.db import models
from helper import AbstractImageModel
from django.utils import timezone
from django.db.models.signals import post_save, m2m_changed
import itertools
from django.utils.text import slugify
from django.db.models import F
from django.utils.encoding import smart_text
from django.conf import settings
from decimal import Decimal
from members.models import PromotionOffer

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


class Product(models.Model):
    sku = models.CharField(max_length=25, null=True, blank=True)
    short_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    description = models.TextField(null=True, blank=True)
    store = models.ForeignKey('merchants.Store')
    manufacturer = models.CharField(max_length=25, null=True, blank=True)
    units = models.IntegerField(default=1)
    url = models.URLField(null=True, blank=True)

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
    tags = models.TextField(null=True, blank=True)  # list of tag words

    # Categorization
    segment = models.ManyToManyField(Segment, null=True, blank=True)
    style = models.ManyToManyField(Style, null=True, blank=True, verbose_name='style')
    furnituretype = models.ManyToManyField(FurnitureType, null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    subcategory = models.ManyToManyField(Subcategory)  # required for has_trial

    # Availability
    added_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    has_trial = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_publishable = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    is_instore = models.BooleanField(default=True)
    delivery_weeks = models.CharField(max_length=100, null=True, blank=True)
    is_avail_now = models.BooleanField(default=True)

    class Meta:
        # added Height as quick hack to randomize display of products as pub_date clusters
        # items by store
        ordering = ['-is_featured', 'short_name', '-pub_date']

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.lat = self.store.lat
        self.lng = self.store.lng

        # Check to see if pub date us missing if item is published.
        if self.is_published and (not self.pub_date):
            self.pub_date = timezone.now()

        self.slug = slugify(self.short_name)
        for x in itertools.count(1):
            if not Product.objects.filter(slug=self.slug).exists():
                break
            # append number to slug if it already exists
            self.slug = '%s-%d' % (self.slug, x)
        super(Product, self).save(*args, **kwargs)

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
        delta = timezone.now() - self.pub_date
        time_lapse = delta.total_seconds() // 3600
        return int(time_lapse)

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


# Funtions created for Product model signals
def does_product_have_trial(sender, instance, **kwargs):
        """if has a price above $1000, it is eligible for a trial
        """
        if instance.current_price >= 1000:
            Product.objects.filter(id=instance.id).update(has_trial=True)

def does_product_have_trial_subcat(sender, instance, **kwargs):
        """if product is part of a subcategory that
        is triable it is eligible for a trial
        """
        trial_list = Subcategory.objects.filter(trial_product=True)
        if instance.subcategory.first() in trial_list:
            Product.objects.filter(id=instance.id).update(has_trial=True)

# post_save methods for Product model to determine if product eligible for buy-and-try
post_save.connect(does_product_have_trial, sender=Product)
m2m_changed.connect(does_product_have_trial_subcat, sender=Product.subcategory.through)


class ProductImage(AbstractImageModel):
    product = models.ForeignKey('goods.Product')

    class Meta:
        app_label = 'goods'

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




