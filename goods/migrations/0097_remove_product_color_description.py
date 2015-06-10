# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0096_remove_product_material_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color_description',
        ),
    ]
