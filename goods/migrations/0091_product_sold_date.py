# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0090_product_list_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
