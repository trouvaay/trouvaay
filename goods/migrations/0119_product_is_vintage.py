# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0118_delete_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_vintage',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
