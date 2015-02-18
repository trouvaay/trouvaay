# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0024_auto_20150217_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuserorderitem',
            name='reservation_expire',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
