# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0043_auto_20150112_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='shipping_charge',
            field=models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, choices=[(0.0, 0.0), (10.0, 10.0), (20.0, 20.0), (50.0, 50.0)]),
            preserve_default=True,
        ),
    ]
