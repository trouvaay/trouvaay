# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0121_auto_20150615_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='rooms',
            field=models.ManyToManyField(to='goods.Room'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='categories',
            field=models.ManyToManyField(to='goods.Category'),
            preserve_default=True,
        ),
    ]
