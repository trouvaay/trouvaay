# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0078_auto_20150307_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_recent',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
