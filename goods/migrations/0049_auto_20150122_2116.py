# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0048_auto_20150122_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_publishable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
