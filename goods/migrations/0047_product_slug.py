# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0046_auto_20150116_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 1, 22, 6, 17, 16, 596467, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
