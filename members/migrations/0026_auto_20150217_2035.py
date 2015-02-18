# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0025_authuserorderitem_reservation_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuserorderitem',
            name='has_open_reservation',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
