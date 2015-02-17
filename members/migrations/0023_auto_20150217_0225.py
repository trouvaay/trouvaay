# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0022_auto_20150211_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuserorder',
            name='authuser',
            field=models.ForeignKey(related_name='user_orders', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='authuserorderitem',
            name='order',
            field=models.ForeignKey(related_name='order_items', blank=True, to='members.AuthUserOrder', null=True),
            preserve_default=True,
        ),
    ]
