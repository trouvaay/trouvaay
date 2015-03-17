# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0036_auto_20150311_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('taxes', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, blank=None, help_text=b'Taxes in dollars', null=None)),
                ('original_price', models.DecimalField(default=0.0, help_text=b'Price of the product at the time of purchase', max_digits=8, decimal_places=2)),
                ('transaction_price', models.DecimalField(default=0.0, help_text=b'Total purchase price the user paid including promotions and taxes', max_digits=8, decimal_places=2)),
                ('offer_price', models.DecimalField(default=0.0, help_text=b'Price offered by user', max_digits=8, decimal_places=2)),
                ('authuser', models.ForeignKey(related_name='offer', to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(related_name='offer', to='members.AuthOrder')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='authorder',
            name='order_type',
            field=models.CharField(db_index=True, max_length=20, choices=[(b'RESERVATION', b'Reservation'), (b'PURCHASE', b'Purchase'), (b'OFFER', b'Offer')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='authuser',
            field=models.ForeignKey(related_name='purchase', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
