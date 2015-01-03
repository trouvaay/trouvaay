# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0021_auto_20150102_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='current_price',
            field=models.DecimalField(max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='original_price',
            field=models.DecimalField(max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
    ]
