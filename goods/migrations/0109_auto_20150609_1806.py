# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0108_remove_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('select', models.CharField(default=b'unspecified', unique=True, max_length=55)),
            ],
            options={
                'ordering': ['select'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('select', models.CharField(default=b'unspecified', unique=True, max_length=55)),
            ],
            options={
                'ordering': ['select'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='category',
            name='select',
            field=models.CharField(default=b'unspecified', unique=True, max_length=55),
            preserve_default=True,
        ),
    ]
