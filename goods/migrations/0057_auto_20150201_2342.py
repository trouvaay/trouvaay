# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0056_auto_20150129_0000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['short_name', '-pub_date']},
        ),
    ]
