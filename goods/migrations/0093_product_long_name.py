# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0092_remove_product_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='long_name',
            field=models.CharField(default=b'tbd', max_length=125),
            preserve_default=True,
        ),
    ]
