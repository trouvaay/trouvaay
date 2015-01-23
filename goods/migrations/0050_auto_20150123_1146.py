# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0049_auto_20150122_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='care',
        ),
        migrations.RemoveField(
            model_name='product',
            name='return_policy',
        ),
        migrations.RemoveField(
            model_name='product',
            name='value_tier',
        ),
    ]
