# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0007_auto_20141213_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailerimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=100, verbose_name='image'),
            preserve_default=True,
        ),
    ]
