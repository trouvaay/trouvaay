# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0084_auto_20150315_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hours_left_to_delist',
            field=models.IntegerField(default=604800, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='days_left',
            field=models.IntegerField(default=604800, null=True, blank=True),
            preserve_default=True,
        ),
    ]
