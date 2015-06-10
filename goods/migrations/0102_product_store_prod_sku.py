# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0101_auto_20150609_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='store_prod_sku',
            field=models.CharField(default=b'0000', max_length=50),
            preserve_default=True,
        ),
    ]
