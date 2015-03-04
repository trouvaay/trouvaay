# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0032_auto_20150228_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='email',
            field=members.models.LowerEmailField(unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
