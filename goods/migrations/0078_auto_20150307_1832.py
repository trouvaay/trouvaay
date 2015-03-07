# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0077_auto_20150307_1829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-is_recent', '-click_count', '-is_featured', 'md5_order']},
        ),
        migrations.RemoveField(
            model_name='product',
            name='delivery_weeks',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_avail_now',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_instore',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_publishable',
        ),
        migrations.AddField(
            model_name='product',
            name='is_recent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
