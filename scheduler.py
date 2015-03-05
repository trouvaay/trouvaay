"""
Created on Mar 3, 2015

@author: sergey@lanasoft.net
"""

from apscheduler.schedulers.blocking import BlockingScheduler
import os
import logging

logging.basicConfig()  # need this so that scheduler is happy, even though we are not using this logger

sched = BlockingScheduler()

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

    from django.utils import timezone
    from members.models import Reservation

    expired_reservations = Reservation.objects.filter(reservation_expiration__lte=timezone.now())

    for reservation in expired_reservations:
        reservation.is_active = False
        reservation.save()
        product = reservation.order.product
        product.is_reserved = False
        product.save()
        print 'Cleared expired reservation for product {0}'.format(product.short_name)

sched.start()
