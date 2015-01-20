# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '__first__'),
        ('members', '0017_auto_20150116_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('registrationprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='registration.RegistrationProfile')),
            ],
            options={
            },
            bases=('registration.registrationprofile',),
        ),
    ]
