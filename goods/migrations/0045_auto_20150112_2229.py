# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0044_subcategory_shipping_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='shipping_charge',
            field=models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, choices=[(5.0, 5.0), (20.0, 20.0), (50.0, 50.0)]),
            preserve_default=True,
        ),
    ]
