# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0082_product_minimum_offer_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='days_left',
            field=models.IntegerField(default=7),
            preserve_default=True,
        ),
    ]
