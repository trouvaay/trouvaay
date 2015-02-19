# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0024_auto_20150217_0225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref_id', models.CharField(unique=True, max_length=120)),
                ('client_id', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('authuser', models.ForeignKey(related_name='user_join', to=settings.AUTH_USER_MODEL)),
                ('friend', models.ForeignKey(related_name='referral', blank=True, to='members.Join', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
