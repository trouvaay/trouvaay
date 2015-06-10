# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0102_product_store_prod_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='the_hunt',
        ),
    ]
