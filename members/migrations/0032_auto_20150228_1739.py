# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0031_auto_20150228_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authusercart',
            name='authuser',
        ),
        migrations.RemoveField(
            model_name='authusercart',
            name='saved_items',
        ),
        migrations.DeleteModel(
            name='AuthUserCart',
        ),
    ]
