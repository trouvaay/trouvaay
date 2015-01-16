# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_auto_20150115_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authuserorder',
            name='captured',
        ),
        migrations.RemoveField(
            model_name='authuserorder',
            name='order_items',
        ),
        migrations.AddField(
            model_name='authuserorderitem',
            name='order',
            field=models.ForeignKey(blank=True, to='members.AuthUserOrder', null=True),
            preserve_default=True,
        ),
    ]
