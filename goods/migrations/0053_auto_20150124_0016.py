# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0052_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='delivery_weeks',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='is_avail_now',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='is_instore',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
