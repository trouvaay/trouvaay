# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_auto_20141218_0925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='material',
            name='description',
        ),
        migrations.RemoveField(
            model_name='segment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='style',
            name='description',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='description',
        ),
        migrations.AddField(
            model_name='category',
            name='option',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='option',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='segment',
            name='option',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='style',
            name='option',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='option',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
    ]
