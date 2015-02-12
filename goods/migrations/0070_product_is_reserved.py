# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0069_auto_20150211_0417'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_reserved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
