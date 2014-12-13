# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0003_auto_20141211_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipper',
            name='store',
        ),
        migrations.AddField(
            model_name='store',
            name='shipper',
            field=models.ManyToManyField(to='merchants.Shipper'),
            preserve_default=True,
        ),
    ]
