# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0028_auto_20150220_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', localflavor.us.models.PhoneNumberField(default=b'', max_length=20, blank=True)),
                ('authuser', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
