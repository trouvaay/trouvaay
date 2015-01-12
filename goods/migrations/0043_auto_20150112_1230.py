# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0042_auto_20150112_0123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='authuser',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='product',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.RemoveField(
            model_name='newproductactivity',
            name='product',
        ),
        migrations.DeleteModel(
            name='NewProductActivity',
        ),
        migrations.RemoveField(
            model_name='vintageproductactivity',
            name='product',
        ),
        migrations.DeleteModel(
            name='VintageProductActivity',
        ),
    ]
