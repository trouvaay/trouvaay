# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0081_auto_20150310_0248'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='minimum_offer_price',
            field=models.DecimalField(default=None, null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
