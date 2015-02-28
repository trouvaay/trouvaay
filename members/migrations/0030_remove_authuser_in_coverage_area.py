# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0029_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authuser',
            name='in_coverage_area',
        ),
    ]
