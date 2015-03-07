# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0075_auto_20150306_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-is_recent', '-click_count', '-is_featured', 'md5_order']},
        ),
        migrations.AddField(
            model_name='product',
            name='is_recent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
