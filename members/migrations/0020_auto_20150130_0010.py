# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0019_promotionoffer_promotionredemption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionoffer',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=5, blank=True, help_text=b'Expressed as percentage, e.g. 10 means 10% off', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='promotionoffer',
            name='short_terms',
            field=models.TextField(help_text=b'This is a short vertion of the terms that we can show to the user e.g. on a front page where they might actually read it.', max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='promotionoffer',
            name='terms',
            field=models.TextField(help_text=b'This is the "fine print", explaining in every details the terms of the promotion', max_length=10000),
            preserve_default=True,
        ),
    ]
