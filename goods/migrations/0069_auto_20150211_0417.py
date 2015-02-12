# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0068_auto_20150210_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='short_name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
