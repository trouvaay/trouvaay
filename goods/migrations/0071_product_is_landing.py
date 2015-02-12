# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0070_product_is_reserved'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_landing',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
