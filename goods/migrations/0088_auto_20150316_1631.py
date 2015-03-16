# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0087_auto_20150315_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='hours_left',
            field=models.IntegerField(default=720, null=True, blank=True),
            preserve_default=True,
        ),
    ]
