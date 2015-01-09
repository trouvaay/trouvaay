from django.db import models

# Create your models here.
class Cart(models.Model):
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "Cart id: {}".format(self.id)

	def get_num_of_items(self):
		return self.cartitem_set.all().count


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, null=True, blank=True)
	product = models.ForeignKey('goods.Product', null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
