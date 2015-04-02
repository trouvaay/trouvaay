# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0038_offer_is_captured'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
