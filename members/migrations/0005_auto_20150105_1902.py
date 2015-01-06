# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_authuseractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuseractivity',
            name='authuser',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
    ]
