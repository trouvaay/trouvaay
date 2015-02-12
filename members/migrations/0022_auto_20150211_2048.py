# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0021_authuserorder_taxes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionoffer',
            name='offer_type',
            field=models.CharField(help_text=b'This field determines how offer is applied: e.g. "First order", or "$10 off towards next purchase', max_length=50, db_index=True, choices=[(b'FIRST_ORDER', b'First order'), (b'DISCOUNT_PROMO', b'Discount promo')]),
            preserve_default=True,
        ),
    ]
