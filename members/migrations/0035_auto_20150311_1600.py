# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0034_auto_20150304_2205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authuser',
            options={'ordering': ['-date_joined']},
        ),
    ]
