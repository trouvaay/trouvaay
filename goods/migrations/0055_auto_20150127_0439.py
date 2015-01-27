# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0054_furnituretype_is_furniture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['height', '-pub_date']},
        ),
    ]
