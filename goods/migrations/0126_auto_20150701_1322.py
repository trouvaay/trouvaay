# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.template.defaultfilters import slugify

def generate_slugs(apps, schema_editor):
    Style = apps.get_model("goods", "Style")
    for style in Style.objects.all():
        style.slug = slugify(style.select)
        style.save()

    Room = apps.get_model("goods", "Room")
    for room in Room.objects.all():
        room.slug = slugify(room.select)
        room.save()

    Category = apps.get_model("goods", "Category")
    for category in Category.objects.all():
        category.slug = slugify(category.select)
        category.save()

class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0125_auto_20150701_1320'),
    ]

    operations = [
            migrations.RunPython(generate_slugs),
    ]
