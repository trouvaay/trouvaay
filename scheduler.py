"""
Created on Mar 3, 2015

@author: sergey@lanasoft.net
"""
from datetime import timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.utils import timezone
import os
import logging


logging.basicConfig()  # need this so that scheduler is happy, even though we are not using this logger

sched = BlockingScheduler()


# runs every hour
@sched.scheduled_job('interval', hours=1)
def update_product_is_recent():
    """Updates product's is_recent flag based on the time"""

    # need the following because we are running
    # this in a stand-alone script
    # not part of the django application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trouvaay.settings.base")
    import django
    django.setup()  # this makes our django models available to our script

    
    from goods.models import Product
    products = Product.objects.all()

    for product in products:
        if(product.pub_date is None):
            continue

        if((product.pub_date <= (timezone.now() - timedelta(hours=settings.RECENT_PRODUCT_AGE))) and product.is_recent):
            product.is_recent = False
            product.save()
            print 'Marked product {0} as not recent'.format(product.short_name)
        elif((product.pub_date > (timezone.now() - timedelta(hours=settings.RECENT_PRODUCT_AGE))) and (not product.is_recent)):
            product.is_recent = True
            product.save()
            print 'Marked product {0} as recent'.format(product.short_name)


@sched.scheduled_job('interval', hours=1)
def update_product_days_left():
    """Updates product's days_left field and unpublishing product
    if days_left is <= 0"""

    # need the following because we are running
    # this in a stand-alone script
    # not part of the django application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trouvaay.settings.base")
    import django
    django.setup()  # this makes our django models available to our script

    
    from goods.models import Product
    products = Product.objects.all()

    for product in products:
        print('working on product {}'.format(product.short_name))
        # skip if product isnt published
        if(not product.is_published):
            print('skipping- its not published')
            continue
        else:
            product.save()


# runs every 5 minutes of every hour of every day
@sched.scheduled_job('cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
def clear_expired_reservations():
    """Sets reservations to be inactive if reservation has expired,
    also makes the reserved product available again.
    """

    # need the following because we are running
    # this in a stand-alone script
    # not part of the django application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trouvaay.settings.base")
    import django
    django.setup()  # this makes our django models available to our script

    from members.models import Reservation
    
    expired_reservations = Reservation.objects.filter(is_active=True, reservation_expiration__lte=timezone.now())

    for reservation in expired_reservations:
        reservation.cancel_reservation()
        print 'Cleared expired reservation for product {0}'.format(reservation.order.product.short_name)


@sched.scheduled_job('interval', hours=1)
def calc_display_score():
    """Calculates display score for all products
    """

     # need the following because we are running
    # this in a stand-alone script
    # not part of the django application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trouvaay.settings.base")
    import django
    django.setup()  # this makes our django models available to our script


    from goods.models import Product
    for product in Product.objects.all():
        product.calc_display_score()


# sched.start()

if __name__ == "__main__":
    clear_expired_reservations()
    update_product_is_recent()
    calc_display_score()
    # update_product_days_left()

