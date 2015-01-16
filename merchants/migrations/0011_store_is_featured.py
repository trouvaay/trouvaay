# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0010_auto_20150112_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_featured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
