# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0083_product_days_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='days_left',
            field=models.IntegerField(default=7, null=True, blank=True),
            preserve_default=True,
        ),
    ]
