"""
Created on Feb 4, 2015

@author: sergey@lanasoft.net
"""

from datetime import datetime
import poplib
import random
import string
import sys
from time import sleep
import unittest

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config

class RaredoorMembers(object):

    # -------------------------------------------------------------------------
    # setup and teardown are part of the unittest framework
    # -------------------------------------------------------------------------
    def setUp(self):
        self.driver = None  # this will be set in a subclass
        random.seed()

    def tearDown(self):
        self.driver.close()


    # -------------------------------------------------------------------------
    # helper functions all start with is_ or do_ or generate_
    # -------------------------------------------------------------------------
    def is_present_by_class(self, driver, class_name):
        """Checks if the element can be located on the page by class
        
        Selenium provides method find_elements_by_class_name, however
        that is not always useful because it creates errors if element is missing
        This function allows us to do a simple presence test
        """
        try:
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            if(element):
                return True
        except TimeoutException:
            pass
        return False

    def is_present_by_id(self, driver, id_):
        """Checks if the element can be located on the page by id
        
        same as is_present_by_class but checks by id
        """
        try:
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, id_))
            )
            if(element):
                return True
        except TimeoutException:
            pass
        return False

    def generate_new_email(self, base_email):
        """Generates new email address from base email address
        by appending "+test<timestamp>" to the user part of email address
        this works ok on gmail addresses
        """

        user, domain = base_email.split('@')
        return '%s+test%s@%s' % (user, datetime.now().strftime('%Y%m%d%H%M%S'), domain)

    def generate_new_password(self, password_length=10):
        """Generates random alphanumeric password"""
        result = ''
        for _i in xrange(password_length):
            result += random.choice(string.ascii_letters + string.digits)
        return result

    def do_login(self, driver, email, password):
        """Helper function to log user in"""
        nav_login = driver.find_elements_by_class_name("nav-login-button")[0]
        webdriver.ActionChains(driver).move_to_element(nav_login).click(nav_login).perform()
        sleep(1)

        email_field = driver.find_element_by_xpath("//form[@id='form-login']/fieldset//input[@id='id_email']")
        email_field.send_keys(email)

        password_field = driver.find_element_by_xpath("//form[@id='form-login']/fieldset//input[@id='id_password']")
        password_field.send_keys(password)

        login_button = driver.find_element_by_xpath("//form[@id='form-login']/fieldset//input[@id='submit-id-button-login']")
        webdriver.ActionChains(driver).move_to_element(login_button).click(login_button).perform()
        sleep(1)
        
    def do_signup(self, driver, email, password, password2):
        nav_login = driver.find_elements_by_class_name("nav-login-button")[0]
        webdriver.ActionChains(driver).move_to_element(nav_login).click(nav_login).perform()
        sleep(1)

        email_field = driver.find_element_by_xpath("//form[@id='form-signup']/fieldset//input[@id='id_email']")
        password_field = driver.find_element_by_xpath("//form[@id='form-signup']/fieldset//input[@id='id_password']")
        password2_field = driver.find_element_by_xpath("//form[@id='form-signup']/fieldset//input[@id='id_password2']")

        email_field.send_keys(email)
        password_field.send_keys(password)
        password2_field.send_keys(password2)

        login_button = driver.find_element_by_xpath("//form[@id='form-signup']/fieldset//input[@id='submit-id-submit']")
        webdriver.ActionChains(driver).move_to_element(login_button).click(login_button).perform()
        sleep(1)

    def do_logout(self, driver):
        nav_login = driver.find_elements_by_class_name("nav-logout-button")[0]
        webdriver.ActionChains(driver).move_to_element(nav_login).click(nav_login).perform()
        sleep(1)        
        
    def do_view_random_product(self, driver):

        # click on "Shop the Bay"
        button_go_shopping = driver.find_elements_by_class_name("button-shop-the-bay")[0]
        webdriver.ActionChains(driver).move_to_element(button_go_shopping).click(button_go_shopping).perform()
        sleep(1)

        # select random product and go to that products details
        random_product = random.choice(driver.find_elements_by_class_name("product-container"))
        random_product_link = random_product.find_elements_by_class_name("view-product")[0]
        webdriver.ActionChains(driver).move_to_element(random_product_link).click(random_product_link).perform()
        sleep(1)

    def do_process_stripe_checkout(self, button, driver, email):

        webdriver.ActionChains(driver).move_to_element(button).click(button).perform()
        sleep(7)

        driver.switch_to.frame('stripe_checkout_app')
        sleep(0.5)

        self.assert_(self.is_present_by_class(driver, "bodyView"), 'Missing stripe checkout modal')

        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("shipping-name").send_keys(config.NEW_USER_SHIPPING_NAME)
        driver.find_element_by_id("shipping-name").send_keys(Keys.SHIFT, Keys.TAB)
        driver.find_element_by_id("shipping-street").send_keys(config.NEW_USER_SHIPPING_STREET)
        driver.find_element_by_id("shipping-zip").send_keys(config.NEW_USER_SHIPPING_ZIP)
        sleep(1)  # autocomplete should fill in the city

        submit_button = driver.find_element_by_id("submitButton")
        webdriver.ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()

        sleep(0.5)  # stripe's pretty UI needs some time to format cc number nicely
        driver.find_element_by_id("card_number").send_keys(config.NEW_USER_CC_NUMBER[0:4])
        sleep(0.5)
        driver.find_element_by_id("card_number").send_keys(config.NEW_USER_CC_NUMBER[4:8])
        sleep(0.5)
        driver.find_element_by_id("card_number").send_keys(config.NEW_USER_CC_NUMBER[8:12])
        sleep(0.5)
        driver.find_element_by_id("card_number").send_keys(config.NEW_USER_CC_NUMBER[12:])
        driver.find_element_by_id("cc-exp").send_keys(config.NEW_USER_CC_EXP[0:2])
        sleep(0.5)
        driver.find_element_by_id("cc-exp").send_keys(config.NEW_USER_CC_EXP[2:])
        driver.find_element_by_id("cc-csc").send_keys(config.NEW_USER_CC_CSC)

        submit_button = driver.find_element_by_id("submitButton")
        webdriver.ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()
        sleep(0.5)
        driver.switch_to.default_content()
        sleep(8)

    def do_get_latest_email(self, email, password):
        """Returns message body of the newest email message"""

        sleep(5)
        pop_conn = poplib.POP3_SSL('pop.gmail.com')
        pop_conn.user(email)
        pop_conn.pass_(password)
        total_messages = len(pop_conn.list()[1])
        latest_message = pop_conn.retr(total_messages)
        message_text = "\n".join(latest_message[1])
        pop_conn.quit()
        return message_text

    def do_check_product_name_and_address(self, driver, message_body):

        product_name = driver.find_element_by_id("reserved-product-name").get_attribute('innerHTML')
        product_name = product_name.strip()
        self.assert_(len(product_name) > 0, 'Product name is empty')
        self.assert_(product_name in message_body, 'Product name [%s] is not in email' % product_name)
        
        product_address = driver.find_element_by_id("reserved-product-store-address").get_attribute('innerHTML').strip()
        for line in product_address.split('\n'):
            line = line.strip()
            line = line.replace('"', '')
            if(not line or ">" in line or "<" in line):
                continue
            self.assert_(line in message_body, 'Address line [%s] is not in email' % line)

    def do_checkout(self, driver, is_auth, is_buy, email, email_password, password):

        if(is_auth):
            # test should run as authenticated
            # login if not yet logged in
            if(not self.is_logged_in(driver)):
                self.do_login(driver, email, password)
        else:
            if(self.is_logged_in(driver)):
                self.do_logout(driver)

        self.do_view_random_product(driver)

        # find buy button
        buttons = driver.find_elements_by_class_name("buy")
        buy_button = None
        button_prefix = 'buy_'
        checkout_button_label = 'Purchase'
        if(not is_buy):
            button_prefix = 'reserve_'
            checkout_button_label = 'Reserve'
        for button in buttons:
            if(button.get_attribute('id').startswith(button_prefix)):
                buy_button = button
                break
        self.assertIsNotNone(buy_button, 'Missing buy button')
        webdriver.ActionChains(driver).move_to_element(buy_button).click(buy_button).perform()
        sleep(1)
        self.assert_(self.is_present_by_id(driver, "pre-checkout-modal-container"), 'Missing pre-checkout modal')

        precheckout_modal = driver.find_element_by_id("pre-checkout-modal-container")
        checkout_button = precheckout_modal.find_element_by_id("button-precheckout-submit")
        self.assert_(checkout_button_label in checkout_button.get_attribute('innerHTML'), 'Button should be called "%s"' % checkout_button_label)

        self.do_process_stripe_checkout(checkout_button, driver, email)

        post_checkout = driver.find_element_by_id("post-checkout-modal")
        self.assert_(post_checkout.is_displayed(), "Missing post-checkout 'Thank you' modal")

        transaction_confirmation = driver.find_element_by_id("product-purchase-buy" if is_buy else "product-purchase-try")
        self.assert_(transaction_confirmation.is_displayed(), "Missing confirmation that product was %s" % ("bought" if is_buy else "reserved"))

        message_text = self.do_get_latest_email(email, email_password)
        self.do_check_product_name_and_address(driver, message_text)

    def do_reservation(self, driver, is_auth, email, email_password=None, password=None):

        if(is_auth):
            # test should run as authenticated
            # login if not yet logged in
            if(not self.is_logged_in(driver)):
                self.do_login(driver, email, password)
        else:
            if(self.is_logged_in(driver)):
                self.do_logout(driver)

        self.do_view_random_product(driver)

        # find buy button
        buttons = driver.find_elements_by_class_name("buy")
        buy_button = None
        button_prefix = 'reserve_'
        checkout_button_label = 'Reserve'

        for button in buttons:
            if(button.get_attribute('id').startswith(button_prefix)):
                buy_button = button
                break

        self.assertIsNotNone(buy_button, 'Missing {0} button'.format(checkout_button_label))
        webdriver.ActionChains(driver).move_to_element(buy_button).click(buy_button).perform()
        sleep(1)
        self.assert_(self.is_present_by_id(driver, "pre-checkout-modal-container"), 'Missing pre-checkout modal')

        if(not is_auth):
            email_field = driver.find_element_by_xpath("//form[@id='form-reserve']//input[@id='id_email']")
            email_field.send_keys(email)
            reserve_button = driver.find_element_by_xpath("//form[@id='form-reserve']//input[@id='button-id-button-reserve']")
            webdriver.ActionChains(driver).move_to_element(reserve_button).click(reserve_button).perform()
            sleep(3)

        # if we are testing an authenticated user then they should either
        # have reached the reservation limit or just did a successful reservation
        reservation_message_elem = driver.find_element_by_id("reservation-status-message")
        if('You cannot reserve any more products' not in reservation_message_elem.get_attribute('innerHTML')):
            # limit is not reached so we should get reservation message
            for i in ['You have ', ' reservtions left', 'Check your email to find out where you can see this amazing piece']:
                self.assert_(i in reservation_message_elem.get_attribute('innerHTML'), 'Missing reservation message')

    def is_logged_in(self, driver):
        return self.is_present_by_class(driver, "nav-logout-button")

    # -------------------------------------------------------------------------
    # all tests start with test_
    # -------------------------------------------------------------------------

    def test_logout(self):
        driver = self.driver
        driver.get(config.HOME_URL)
        
        # login if currently not logged in
        if(not self.is_logged_in(driver)):
            self.do_login(driver, config.EXISTING_USER_EMAIL, config.EXISTING_USER_PASSWORD)

        self.do_logout(driver)
        self.assert_(not self.is_present_by_class(driver, "nav-logout-button"), 'Logout button shows up after logout')
        

    def test_login_modal(self):
        """
        check login modal is not present before we clicked on login
        click on login
        check login modal is present after we clicked on login
        """

        driver = self.driver
        driver.get(config.HOME_URL)

        if(self.is_logged_in(driver)):
            self.do_logout(driver)

        self.assert_(not self.is_present_by_id(driver, "form-login"), "Login form shows up before we clicked on login")

        nav_login = driver.find_elements_by_class_name("nav-login-button")[0]
        webdriver.ActionChains(driver).move_to_element(nav_login).click(nav_login).perform()

        self.assert_(self.is_present_by_id(driver, "form-login"), "No login form after click on login")

    def test_login_valid(self):
        """
        login with existing user username/password
        """
        driver = self.driver
        driver.get(config.HOME_URL)

        if(self.is_logged_in(driver)):
            self.do_logout(driver)

        self.do_login(driver, config.EXISTING_USER_EMAIL, config.EXISTING_USER_PASSWORD)
        self.assert_(not self.is_present_by_id(driver, "form-login"), "Login form showed up again after successful login")
        self.assert_(self.is_present_by_class(driver, "nav-logout-button"), "No logout button after successful login")
        
    def test_login_invalid(self):
        """
        try to login with invalid username/password
        """

        driver = self.driver
        driver.get(config.HOME_URL)

        if(self.is_logged_in(driver)):
            self.do_logout(driver)

        # use real existing user and randomly generated password that is longer than
        # the real password, which will always make it invalid
        self.do_login(driver=driver,
                      email=config.EXISTING_USER_EMAIL,
                      password=self.generate_new_password(password_length=len(config.EXISTING_USER_PASSWORD) + 1))
        self.assert_(self.is_present_by_id(driver, "form-login"), "No login form after invalid login")
        self.assert_(not self.is_present_by_class(driver, "nav-logout-button"), "Logout button shows up after invalid login")


    def test_signup_modal(self):
        """make sure signup modal shows up"""
        driver = self.driver
        driver.get(config.HOME_URL)

        # logout if already logged in
        if(self.is_logged_in(driver)):
            self.do_logout(driver)

        nav_login = driver.find_elements_by_class_name("nav-login-button")[0]

        webdriver.ActionChains(driver).move_to_element(nav_login).click(nav_login).perform()
        sleep(1)

        form_signup = driver.find_element_by_id("form-signup")
        self.assertIsNotNone(form_signup, 'did not find signup form after click on login')

    def test_signup_invalid_existing_email(self):
        """try to signup with email that already exists"""
        driver = self.driver
        driver.get(config.HOME_URL)

        # logout if already logged in
        if(self.is_logged_in(driver)):
            self.do_logout(driver)

        # we are testing existing email here, passwords do not matter
        self.do_signup(driver, config.EXISTING_USER_EMAIL, '123', '123')
        self.assert_(self.is_present_by_id(driver, "error_1_id_email"), "Signup with existing user's email should have failed")
        error_elem = driver.find_element_by_id("error_1_id_email")
        self.assert_('Auth user with this Email already exists.' in error_elem.get_attribute('innerHTML'), 'Missing existing email error message')

    def test_signup_invalid_passwords_do_not_match(self):
        driver = self.driver
        driver.get(config.HOME_URL)

        # logout if already logged in
        if(self.is_logged_in(driver)):
            self.do_logout(driver)

        email = self.generate_new_email(config.NEW_USER_BASE_EMAIL)
        password = self.generate_new_password(password_length=10)
        self.do_signup(driver, email, password, password[:-1])
        self.assert_(self.is_present_by_id(driver, "error_1_id_password"), "Signup with mismatched passwords should have failed")
        error_elem = driver.find_element_by_id("error_1_id_password")
        self.assert_('Your passwords should match.' in error_elem.get_attribute('innerHTML'), 'Missing mismatched passwords error message')

    def test_signup_valid(self):
        driver = self.driver
        driver.get(config.HOME_URL)

        # logout if already logged in
        if(self.is_logged_in(driver)):
            self.do_logout(driver)

        email = self.generate_new_email(config.NEW_USER_BASE_EMAIL)
        password = self.generate_new_password(password_length=10)
        self.do_signup(driver, email, password, password)
        sleep(3)
        body_elem = driver.find_element_by_xpath("//body")
        self.assert_('Account Created - Welcome!' in body_elem.get_attribute('innerHTML'), 'Missing success message')

        # click away from modal to dismiss it
        webdriver.ActionChains(driver).move_by_offset(0, -200).click().perform()
        sleep(1)

        # logout and then do login for newly created user
        if(self.is_logged_in(driver)):
            self.do_logout(driver)
        sleep(1)

        driver.get(config.HOME_URL)

        self.do_login(driver, email, password)
        self.assert_(self.is_present_by_class(driver, "nav-logout-button"), "Login failed for newly created user")

    def test_buy_product_auth(self):
        """Buy product as authenticated user"""
        driver = self.driver
        driver.get(config.HOME_URL)

        self.do_checkout(driver=driver, is_auth=True, is_buy=True,
                         email=config.EXISTING_USER_EMAIL,
                         email_password=config.EXISTING_USER_EMAIL_PASSWORD,
                         password=config.EXISTING_USER_PASSWORD)

    def test_buy_product_nonauth(self):
        """Buy product as non-authenticated existing user"""
        driver = self.driver
        driver.get(config.HOME_URL)

        self.do_checkout(driver=driver, is_auth=False, is_buy=True,
                         email=config.EXISTING_USER_EMAIL,
                         email_password=config.EXISTING_USER_EMAIL_PASSWORD,
                         password=config.EXISTING_USER_PASSWORD)

    def test_reserve_product_auth(self):
        """Reserve product as authenticated user"""
        driver = self.driver
        driver.get(config.HOME_URL)

        self.do_reservation(driver=driver, is_auth=True,
                            email=config.EXISTING_USER_EMAIL,
                            email_password=config.EXISTING_USER_EMAIL_PASSWORD,
                            password=config.EXISTING_USER_PASSWORD)



    def test_reserve_product_nonauth(self):
        """Reserve product as non-authenticated existing user"""
        driver = self.driver
        driver.get(config.HOME_URL)

        self.do_reservation(driver=driver, is_auth=False, email=config.EXISTING_USER_EMAIL)

    def test_reserve_product_newuser(self):
        """Reserve product as a non-registered user"""
        driver = self.driver
        driver.get(config.HOME_URL)

        self.do_reservation(driver=driver, is_auth=False, email=self.generate_new_email(config.NEW_USER_BASE_EMAIL))


class ChromeTests(RaredoorMembers, unittest.TestCase):
    def setUp(self):
        super(ChromeTests, self).setUp()
        self.driver = webdriver.Chrome()


class FirefoxTests(RaredoorMembers, unittest.TestCase):
    def setUp(self):
        super(FirefoxTests, self).setUp()
        self.driver = webdriver.Firefox()
