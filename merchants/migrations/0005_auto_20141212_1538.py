# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0004_auto_20141212_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='description',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='store',
            name='shipper',
            field=models.ManyToManyField(blank=True, to='merchants.Shipper', null=True),
            preserve_default=True,
        ),
    ]
