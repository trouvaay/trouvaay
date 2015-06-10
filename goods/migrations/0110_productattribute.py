# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0109_auto_20150609_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('width', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('depth', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('height', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('seat_height', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('bed_size', models.CharField(max_length=50, null=True, blank=True)),
                ('weight', models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True)),
                ('is_vintage', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, to='goods.Category', null=True)),
                ('color', models.ManyToManyField(to='goods.Color', null=True, blank=True)),
                ('group', models.ForeignKey(blank=True, to='goods.Group', null=True)),
                ('material', models.ManyToManyField(to='goods.Material', null=True, blank=True)),
                ('product', models.ForeignKey(to='goods.Product')),
                ('room', models.ManyToManyField(to='goods.Room', null=True, blank=True)),
                ('style', models.ManyToManyField(to='goods.Style', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
