# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0037_auto_20150110_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_trial',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
