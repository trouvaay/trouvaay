# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_authuser_in_coverage_area'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authuseractivity',
            options={'ordering': ['authuser']},
        ),
    ]
