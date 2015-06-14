# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0111_auto_20150609_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='product',
            name='reserve_price',
            field=models.DecimalField(default=None, null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
