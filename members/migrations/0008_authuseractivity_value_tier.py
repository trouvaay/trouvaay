# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0032_valuetier'),
        ('members', '0007_auto_20150108_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuseractivity',
            name='value_tier',
            field=models.ManyToManyField(to='goods.ValueTier'),
            preserve_default=True,
        ),
    ]
