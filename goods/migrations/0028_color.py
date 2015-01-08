# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0027_product_furnituretype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('select', models.CharField(default=b'blue', max_length=55, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
