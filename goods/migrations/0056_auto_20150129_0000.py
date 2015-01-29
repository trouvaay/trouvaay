# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0055_auto_20150127_1932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['height', '-pub_date']},
        ),
    ]
