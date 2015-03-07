"""
Created on Mar 3, 2015

@author: sergey@lanasoft.net
"""

from datetime import timedelta
import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler


logging.basicConfig()  # need this so that scheduler is happy, even though we are not using this logger

sched = BlockingScheduler()

# runs every hour
@sched.scheduled_job('interval', hours=1)
def update_product_is_recent():
    """Updates product's is_recent flag based on the time
    """

    # need the following because we are running
    # this in a stand-alone script
    # not part of the django application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trouvaay.settings.base")
    import django
    django.setup()  # this makes our django models available to our script

    from django.utils import timezone
    from django.conf import settings
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

sched.start()
