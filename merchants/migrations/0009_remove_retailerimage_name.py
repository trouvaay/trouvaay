# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0008_auto_20141222_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retailerimage',
            name='name',
        ),
    ]
