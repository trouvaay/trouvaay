# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0030_remove_authuser_in_coverage_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authuserstripe',
            name='authuser',
        ),
        migrations.DeleteModel(
            name='AuthUserStripe',
        ),
    ]
