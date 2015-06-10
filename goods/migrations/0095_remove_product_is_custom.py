# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0094_auto_20150609_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_custom',
        ),
    ]
