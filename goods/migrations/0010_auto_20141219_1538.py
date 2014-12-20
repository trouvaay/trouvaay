# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_auto_20141219_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='option',
            new_name='select',
        ),
        migrations.RenameField(
            model_name='material',
            old_name='option',
            new_name='select',
        ),
        migrations.RenameField(
            model_name='segment',
            old_name='option',
            new_name='select',
        ),
        migrations.RenameField(
            model_name='style',
            old_name='option',
            new_name='select',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='option',
            new_name='select',
        ),
    ]
