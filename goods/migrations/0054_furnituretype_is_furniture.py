# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0053_auto_20150124_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='furnituretype',
            name='is_furniture',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
