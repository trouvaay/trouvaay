# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0120_auto_20150615_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='reserve_price',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
