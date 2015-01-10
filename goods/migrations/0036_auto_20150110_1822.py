# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0035_auto_20150110_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='long_name',
        ),
        migrations.AlterField(
            model_name='product',
            name='short_name',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
