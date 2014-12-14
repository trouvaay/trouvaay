# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0006_retailerimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailerimage',
            name='is_main',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
