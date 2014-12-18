# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_auto_20141218_0924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='Message',
            new_name='message',
        ),
    ]
