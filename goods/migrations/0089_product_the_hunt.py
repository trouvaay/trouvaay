# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0088_auto_20150316_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='the_hunt',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
