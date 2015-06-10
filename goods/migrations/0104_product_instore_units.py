# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0103_remove_product_the_hunt'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='instore_units',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
