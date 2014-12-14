# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20141213_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('image', models.ImageField(upload_to='photos/%y/%m/%d/')),
                ('is_main', models.BooleanField()),
                ('product', models.ForeignKey(to='goods.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
