# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0097_remove_product_color_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_featured',
        ),
    ]
