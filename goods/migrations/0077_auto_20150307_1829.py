# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0076_auto_20150307_0019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-click_count', '-is_featured', 'md5_order']},
        ),
        migrations.RemoveField(
            model_name='product',
            name='has_trial',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_recent',
        ),
    ]
