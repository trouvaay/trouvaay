# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0113_remove_product_minimum_offer_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='room',
            field=models.ManyToManyField(to='goods.Room', null=True, blank=True),
            preserve_default=True,
        ),
    ]
