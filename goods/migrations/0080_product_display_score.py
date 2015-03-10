# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0079_auto_20150308_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='display_score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
