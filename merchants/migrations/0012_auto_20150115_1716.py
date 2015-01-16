# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0011_store_is_featured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ['retailer', 'street']},
        ),
    ]
