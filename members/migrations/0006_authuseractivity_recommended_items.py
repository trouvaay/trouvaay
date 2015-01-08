# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0031_auto_20150108_0121'),
        ('members', '0005_auto_20150105_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuseractivity',
            name='recommended_items',
            field=models.ManyToManyField(related_name='recommended', to='goods.Product'),
            preserve_default=True,
        ),
    ]
