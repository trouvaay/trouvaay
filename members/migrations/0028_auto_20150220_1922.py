# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0027_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuserorderitem',
            name='has_open_reservation',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
