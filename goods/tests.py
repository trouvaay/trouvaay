from django.test import TestCase
from models import Product, Subcategory
from merchants.models import Store, Retailer
from members.models import AuthUser

'testy'

class ProductTestCase(TestCase):
	def setUp(self):
		test_user = AuthUser.objects.create_user(email='shopper@gmail.com', password='tickle')
		test_retailer = Retailer.objects.create(legal_name='acme industries', \
						short_name='acme', organization_type='indiv', owner=test_user)
		test_store = Store.objects.create(retailer=test_retailer, street='123 street', city='SF',\
											state='CA', zipcd=94040)

		trial_subcategory = Subcategory.objects.create(select='sofa', trial_product=True)
		nontrial_subcategory = Subcategory.objects.create(select='chair')
		
	
	def test_product_saves_as_has_trial_above_price(self):
		"""product saves as trial when is either above 
			price threshold or is in one of the trial
			subcategories
		"""

		#Test that price above $1000 triggers trial attribute
		high_price_prod = Product.objects.create(short_name='test_product1',current_price=1000,\
								store=Store.objects.first())
		high_price_prod.save()
		self.assertTrue(high_price_prod.has_trial)


		low_price_prod = Product.objects.create(short_name='test_product1',current_price=999,\
								store=Store.objects.first())
		low_price_prod.save()
		self.assertFalse(low_price_prod.has_trial)
		
	def test_product_saves_as_has_trial_when_in_trial_subcateogry(self):
		"""If product is priced under $1,000 it should save as
			has_trial when its tagged with a subcategory with
			trial_product = True
		"""
		
		#Test that product having a 'trial_product' ==True field triggers trial product
		trial_subcat = Subcategory.objects.get(trial_product=True)
		nontrial_subcat = Subcategory.objects.get(trial_product=False)

		prod_nontrial_subcat = Product.objects.create(short_name='test_product1',current_price=999,\
								store=Store.objects.first())
		prod_nontrial_subcat.subcategory.add(nontrial_subcat)
		prod_nontrial_subcat.save()
		self.assertFalse(prod_nontrial_subcat.has_trial)

		prod_trial_subcat = Product.objects.create(short_name='test_product1',current_price=999,\
								store=Store.objects.first())
		prod_trial_subcat.subcategory.add(trial_subcat)
		prod_trial_subcat.save()
		self.assertTrue(prod_trial_subcat.has_trial)

	def test_create_new_shopper_added_to_db(self):
		""" Test if email saved to db properly"""
		shopper = AuthUser.objects.get(email='shopper@gmail.com')
		self.assertEqual(AuthUser.objects.all()[0].email,'shopper@gmail.com')
