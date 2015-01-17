# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0045_auto_20150112_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(to='goods.Subcategory'),
            preserve_default=True,
        ),
    ]
