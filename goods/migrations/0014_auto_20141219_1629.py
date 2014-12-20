# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0013_auto_20141219_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='select',
            field=models.CharField(blank=True, null=True, default='living', max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='select',
            field=models.CharField(blank=True, null=True, default='leather', max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='segment',
            name='select',
            field=models.CharField(blank=True, null=True, default='new', max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='style',
            name='select',
            field=models.CharField(blank=True, null=True, default='modern', max_length=55),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='select',
            field=models.CharField(blank=True, null=True, default='bar', max_length=55),
            preserve_default=True,
        ),
    ]
