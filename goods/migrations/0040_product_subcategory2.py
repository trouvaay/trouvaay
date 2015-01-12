# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0039_subcategory_trial_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory2',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'armoire', b'armoire'), (b'bar', b'bar'), (b'bar stool', b'bar stool'), (b'bed', b'bed'), (b'bedding', b'bedding'), (b'bench', b'bench'), (b'chair', b'chair'), (b'chaise', b'chaise'), (b'decor - wall', b'decor - wall'), (b'decor - table', b'decor - table'), (b'decor - other', b'decor - other'), (b'desk', b'desk'), (b'desk light', b'desk light'), (b'dining table', b'dining table'), (b'dresser', b'dresser'), (b'kitchen serving', b'kitchen serving'), (b'lighting - floor', b'lighting - floor'), (b'lighting - table', b'lighting - table'), (b'lighting - other', b'lighting - other'), (b'loveseat', b'loveseat'), (b'media', b'media'), (b'mirror', b'mirror'), (b'ottoman', b'ottoman'), (b'pillow', b'pillow'), (b'rug throw', b'rug throw'), (b'sofa', b'sofa'), (b'storage', b'storage'), (b'table - small', b'table - small'), (b'trunk', b'trunk'), (b'table', b'table')]),
            preserve_default=True,
        ),
    ]
