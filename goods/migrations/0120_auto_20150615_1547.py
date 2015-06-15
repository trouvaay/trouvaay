# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0119_product_is_vintage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='category',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='color',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='group',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='material',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='room',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='style',
        ),
        migrations.DeleteModel(
            name='ProductAttribute',
        ),
    ]
