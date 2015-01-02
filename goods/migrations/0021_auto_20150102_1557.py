# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0020_auto_20150102_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='dimensions',
        ),
        migrations.AddField(
            model_name='product',
            name='is_sold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
