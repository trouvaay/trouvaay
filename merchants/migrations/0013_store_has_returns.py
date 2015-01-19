# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0012_auto_20150115_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='has_returns',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
