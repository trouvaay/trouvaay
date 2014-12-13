# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('members', '0003_auto_20141211_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUserActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('authuser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('saved_items', models.ManyToManyField(to='goods.Product')),
                ('style', models.ManyToManyField(to='goods.Style')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
