# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20141213_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='last_comm_date',
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=50, choices=[('living', 'living'), ('dining', 'dining'), ('bedroom', 'bedroom'), ('office', 'office'), ('lightning', 'lightning'), ('decor', 'decor'), ('other', 'other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='style',
            field=models.ManyToManyField(to='goods.Style', verbose_name='style', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='description',
            field=models.CharField(max_length=50, choices=[('bar', 'bar'), ('bar_stool', 'bar_stool'), ('bed', 'bed'), ('bedding', 'bedding'), ('bench', 'bench'), ('chair', 'chair'), ('chaise', 'chaise'), ('desk', 'desk'), ('desk_light', 'desk_light'), ('dining_table', 'dining_table'), ('floor_lamp', 'floor_lamp'), ('kitchen_serving', 'kitchen_serving'), ('loveseat', 'loveseat'), ('media', 'media'), ('mirror', 'mirror'), ('nightstand', 'nightstand'), ('ottoman', 'ottoman'), ('other_lighting', 'other_lighting'), ('pillow', 'pillow'), ('rug_throw', 'rug_throw'), ('small_table', 'small_table'), ('sofa', 'sofa'), ('storage', 'storage'), ('wall_decor', 'wall_decor')]),
            preserve_default=True,
        ),
    ]
