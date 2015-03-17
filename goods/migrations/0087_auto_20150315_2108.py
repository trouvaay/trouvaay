# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0086_remove_product_days_left'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='hours_left_to_delist',
        ),
        migrations.AddField(
            model_name='product',
            name='hours_left',
            field=models.IntegerField(default=168, null=True, blank=True),
            preserve_default=True,
        ),
    ]
