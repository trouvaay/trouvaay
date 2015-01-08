# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0031_auto_20150108_0121'),
        ('members', '0006_authuseractivity_recommended_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuseractivity',
            name='color',
            field=models.ManyToManyField(to='goods.Color'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='authuseractivity',
            name='furnituretype',
            field=models.ManyToManyField(to='goods.FurnitureType'),
            preserve_default=True,
        ),
    ]
