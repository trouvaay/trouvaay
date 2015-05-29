# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0041_offer_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='is_product_admin',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
