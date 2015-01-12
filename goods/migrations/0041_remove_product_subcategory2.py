# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0040_product_subcategory2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='subcategory2',
        ),
    ]
