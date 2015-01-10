# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_authusercart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuseractivity',
            name='color',
            field=models.ManyToManyField(to='goods.Color', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='authuseractivity',
            name='furnituretype',
            field=models.ManyToManyField(to='goods.FurnitureType', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='authuseractivity',
            name='saved_items',
            field=models.ManyToManyField(to='goods.Product', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='authuseractivity',
            name='style',
            field=models.ManyToManyField(to='goods.Style', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='authuseractivity',
            name='value_tier',
            field=models.ManyToManyField(to='goods.ValueTier', null=True, blank=True),
            preserve_default=True,
        ),
    ]
