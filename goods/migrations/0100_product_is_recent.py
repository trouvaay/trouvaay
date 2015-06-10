# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0099_remove_product_is_recent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_recent',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
