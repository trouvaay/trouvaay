# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0085_auto_20150315_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='days_left',
        ),
    ]
