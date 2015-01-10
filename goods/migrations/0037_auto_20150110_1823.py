# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0036_auto_20150110_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bed_size',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
