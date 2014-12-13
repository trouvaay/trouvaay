# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchants', '0005_auto_20141212_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=50, choices=[('living', 'living'), ('dining', 'dining'), ('bedroom', 'bedroom'), ('office', 'office'), ('bathroom', 'bathroom'), ('outdoor', 'outdoor'), ('baby_children', 'baby_children'), ('lightning', 'lightning'), ('wall_decor', 'wall_decor'), ('general_decor', 'general_decor')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('Message', models.CharField(max_length=255)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('last_comm_date', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField()),
                ('authuser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=50, choices=[('acrylic', 'acrylic'), ('cotton', 'cotton'), ('engineered_wood', 'engineered_wood'), ('leather', 'leather'), ('linen', 'linen'), ('other_fabric', 'other_fabric'), ('polyester', 'polyester'), ('wood_veneer', 'wood_veneer')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewProductActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('likes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('units_sold', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('sku', models.CharField(max_length=25, blank=True, null=True)),
                ('long_name', models.CharField(max_length=50, blank=True, null=True)),
                ('short_name', models.CharField(max_length=25)),
                ('original_price', models.IntegerField()),
                ('current_price', models.IntegerField()),
                ('manufacturer', models.CharField(max_length=25, blank=True, null=True)),
                ('units', models.IntegerField(default=1)),
                ('care', models.TextField(blank=True, null=True)),
                ('dimensions', djorm_pgarray.fields.IntegerArrayField(dimension=3)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('return_policy', models.TextField(blank=True, null=True)),
                ('color', models.CharField(max_length=20, blank=True, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField()),
                ('is_published', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(to='goods.Category')),
                ('marterial', models.ManyToManyField(to='goods.Material')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=50, choices=[('new', 'new'), ('vintage', 'vintage')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=50, choices=[('modern', 'modern'), ('traditional', 'traditional'), ('contemporary', 'contemporary'), ('rustic', 'rustic'), ('industrial', 'industrial'), ('beach', 'beach')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=50, choices=[('bar', 'bar'), ('bar_stool', 'bar_stool'), ('bed', 'bed'), ('bedding', 'bedding'), ('bench', 'bench'), ('chair', 'chair'), ('chaise', 'chaise'), ('desk', 'desk'), ('desk_light', 'desk_light'), ('dining_table', 'dining_table'), ('floor_lamp', 'floor_lamp'), ('kitchen_serving', 'kitchen_serving'), ('media', 'media'), ('mirror', 'mirror'), ('nightstand', 'nightstand'), ('ottoman', 'ottoman'), ('other_lighting', 'other_lighting'), ('pillow', 'pillow'), ('rug_throw', 'rug_throw'), ('small_table', 'small_table'), ('sofa', 'sofa'), ('storage', 'storage'), ('wall_decor', 'wall_decor')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VintageProductActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('likes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('time_to_sale', models.IntegerField(default=0)),
                ('product', models.ForeignKey(to='goods.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='segment',
            field=models.ManyToManyField(to='goods.Segment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(to='merchants.Store'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='style',
            field=models.ManyToManyField(to='goods.Style'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='subcateogry',
            field=models.ManyToManyField(to='goods.Subcategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newproductactivity',
            name='product',
            field=models.ForeignKey(to='goods.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(to='goods.Product'),
            preserve_default=True,
        ),
    ]
