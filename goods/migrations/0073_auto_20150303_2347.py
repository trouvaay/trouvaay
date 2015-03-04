# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0072_auto_20150303_1355'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-click_count']},
        ),
        migrations.AddField(
            model_name='product',
            name='click_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
