# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0011_auto_20141219_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='segment',
        ),
        migrations.DeleteModel(
            name='Segment',
        ),
    ]
