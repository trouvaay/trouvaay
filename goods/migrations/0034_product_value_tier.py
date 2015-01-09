# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0033_auto_20150108_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='value_tier',
            field=models.ForeignKey(blank=True, to='goods.ValueTier', null=True),
            preserve_default=True,
        ),
    ]
