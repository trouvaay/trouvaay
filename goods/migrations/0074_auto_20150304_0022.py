# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0073_auto_20150303_2347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-click_count', '-is_featured', 'md5_order']},
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_hot',
        ),
    ]
