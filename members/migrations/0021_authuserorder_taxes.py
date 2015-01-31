# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0020_auto_20150130_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuserorder',
            name='taxes',
            field=models.DecimalField(default=0.0, null=None, max_digits=8, decimal_places=2, blank=None),
            preserve_default=True,
        ),
    ]
