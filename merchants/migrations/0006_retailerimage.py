# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0005_auto_20141212_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetailerImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('image', models.ImageField(upload_to='photos/%y/%m/%d/')),
                ('is_main', models.BooleanField()),
                ('is_logo', models.BooleanField(default=False)),
                ('retailer', models.ForeignKey(to='merchants.Retailer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
