# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0117_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subcategory',
        ),
    ]
