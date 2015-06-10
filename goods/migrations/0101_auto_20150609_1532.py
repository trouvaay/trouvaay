# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0100_product_is_recent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='hours_left',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_landing',
        ),
    ]
