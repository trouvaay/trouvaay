# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0060_auto_20150205_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(to='goods.Subcategory', null=True, blank=True),
            preserve_default=True,
        ),
    ]
