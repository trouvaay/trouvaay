# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0089_product_the_hunt'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='list_price',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
    ]
