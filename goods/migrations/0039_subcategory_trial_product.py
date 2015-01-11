# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0038_product_has_trial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='trial_product',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
