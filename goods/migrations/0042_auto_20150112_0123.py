# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0041_remove_product_subcategory2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['select']},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['select']},
        ),
        migrations.AlterModelOptions(
            name='furnituretype',
            options={'ordering': ['select']},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['select']},
        ),
        migrations.AlterModelOptions(
            name='segment',
            options={'ordering': ['select']},
        ),
        migrations.AlterModelOptions(
            name='style',
            options={'ordering': ['select']},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['select']},
        ),
        migrations.AlterModelOptions(
            name='valuetier',
            options={'ordering': ['select']},
        ),
        migrations.AlterField(
            model_name='category',
            name='select',
            field=models.CharField(default=b'living', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='color',
            name='select',
            field=models.CharField(default=b'blue', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='furnituretype',
            name='select',
            field=models.CharField(default=b'seating', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='select',
            field=models.CharField(default=b'leather', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='segment',
            name='select',
            field=models.CharField(default=b'new', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='style',
            name='select',
            field=models.CharField(default=b'modern', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='select',
            field=models.CharField(default=b'bar', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='valuetier',
            name='select',
            field=models.CharField(default=b'mid', max_length=55, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
