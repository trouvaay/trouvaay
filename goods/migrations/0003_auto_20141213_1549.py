# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20141212_1816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='subcateogry',
            new_name='subcategory',
        ),
    ]
