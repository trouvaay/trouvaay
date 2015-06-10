# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0105_remove_product_units'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_floor_model',
        ),
    ]
