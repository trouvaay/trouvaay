# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_auto_20141219_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='select',
            field=models.CharField(null=True, blank=True, max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='select',
            field=models.CharField(null=True, blank=True, max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='segment',
            name='select',
            field=models.CharField(null=True, blank=True, max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='style',
            name='select',
            field=models.CharField(null=True, blank=True, max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='select',
            field=models.CharField(null=True, blank=True, max_length=55),
            preserve_default=True,
        ),
    ]
