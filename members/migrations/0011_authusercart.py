# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0034_product_value_tier'),
        ('members', '0010_authuserstripe'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUserCart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('authuser', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
                ('saved_items', models.ManyToManyField(to='goods.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
