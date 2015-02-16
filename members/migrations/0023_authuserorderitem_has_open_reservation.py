# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0022_auto_20150211_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuserorderitem',
            name='has_open_reservation',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
