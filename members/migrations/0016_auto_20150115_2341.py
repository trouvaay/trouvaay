# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_auto_20150115_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuserorderitem',
            name='capture_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='authuserorderitem',
            name='captured',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
