# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0039_offer_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='is_active',
        ),
    ]
