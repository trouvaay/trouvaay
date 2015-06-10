# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0095_remove_product_is_custom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='material_description',
        ),
    ]
