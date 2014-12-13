# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20141211_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='is_merchant',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
