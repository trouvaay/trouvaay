# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0037_auto_20150312_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_captured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
