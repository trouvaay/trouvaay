# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0045_auto_20150112_2229'),
        ('members', '0014_auto_20150115_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUserOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('captured', models.BooleanField(default=True)),
                ('authuser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUserOrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sell_price', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(to='goods.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='authuserorder',
            name='order_items',
            field=models.ManyToManyField(to='members.AuthUserOrderItem'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='authuseractivity',
            name='recommended_items',
            field=models.ManyToManyField(related_name='recommended', null=True, to='goods.Product', blank=True),
            preserve_default=True,
        ),
    ]
