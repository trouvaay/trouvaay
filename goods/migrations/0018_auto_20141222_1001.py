# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0017_auto_20141219_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=100, verbose_name='image'),
            preserve_default=True,
        ),
    ]
