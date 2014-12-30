from django.test import TestCase
from django.contrib.auth.hashers import check_password
from members.models import AuthUser
from django.utils import timezone


class AuthUserTestCase(TestCase):
	def setUp(self):
		AuthUser.objects.create_user(email='shopper@gmail.com', password='tickle')
		AuthUser.objects.create_user(email='merchant@gmail.com', password='nickle')
		

	def test_create_new_shopper_added_to_db(self):
		""" Test if email saved to db properly"""
		shopper = AuthUser.objects.get(email='shopper@gmail.com')
		self.assertEqual(AuthUser.objects.all()[0].email,'shopper@gmail.com')

	def test_if_new_shopper_has_proper_auths(self):
		""" See if new shopper creates as expected with is_active=True, 
			is_merchant=False, is_admin=False, is_staff()=False"""
		
		shopper = AuthUser.objects.get(email='shopper@gmail.com')
		self.assertEqual(shopper.is_admin, False)
		self.assertEqual(shopper.is_staff, False)
		self.assertEqual(shopper.is_superuser, False)

	def test_if_new_shopper_is_active_by_default(self):
		shopper = AuthUser.objects.get(email='shopper@gmail.com')
		self.assertEqual(shopper.is_active, True)
	
	def test_if_new_added_member_is_not_merchant_by_default(self):
		shopper = AuthUser.objects.get(email='shopper@gmail.com')
		self.assertEqual(shopper.is_merchant, False)

	def test_date_joined_field_for_new_added_member(self):
		"""Test password reset method"""
		shopper = AuthUser.objects.get(email='shopper@gmail.com')
		shopper.set_password('pickle')
		self.assertTrue(check_password('pickle',shopper.password))

	