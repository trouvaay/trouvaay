# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20141213_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(null=True, blank=True, to='goods.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='material',
            field=models.ManyToManyField(null=True, blank=True, to='goods.Material'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='segment',
            field=models.ManyToManyField(null=True, blank=True, to='goods.Segment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='style',
            field=models.ManyToManyField(null=True, blank=True, to='goods.Style'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(null=True, blank=True, to='goods.Subcategory'),
            preserve_default=True,
        ),
    ]
