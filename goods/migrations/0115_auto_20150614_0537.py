# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0114_product_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='group',
            field=models.ForeignKey(blank=True, to='goods.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='reserve_price',
            field=models.DecimalField(default=0.0, null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
