# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0030_remove_product_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='colors',
            new_name='color',
        ),
    ]
