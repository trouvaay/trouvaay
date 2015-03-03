# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0071_product_is_landing'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-is_hot', '-is_featured', 'md5_order', 'short_name', '-pub_date']},
        ),
        migrations.AddField(
            model_name='product',
            name='is_hot',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
