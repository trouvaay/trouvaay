# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0016_auto_20141219_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='lat',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='lng',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
