# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0112_auto_20150614_0528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='minimum_offer_price',
        ),
    ]
