# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0071_product_is_landing'),
        ('members', '0033_auto_20150228_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('order_type', models.CharField(db_index=True, max_length=20, choices=[(b'RESERVATION', b'Reservation'), (b'PURCHASE', b'Purchase')])),
                ('converted_from_reservation', models.BooleanField(default=False)),
                ('authuser', models.ForeignKey(related_name='user_orders', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(related_name='product_orders', to='goods.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=50)),
                ('street2', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=2, choices=[(b'AK', b'Alaska'), (b'AL', b'Alabama'), (b'AR', b'Arkansas'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DC', b'District of Columbia'), (b'DE', b'Delaware'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'IA', b'Iowa'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'MA', b'Massachusetts'), (b'MD', b'Maryland'), (b'ME', b'Maine'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MO', b'Missouri'), (b'MP', b'Northern Mariana Islands'), (b'MS', b'Mississippi'), (b'MT', b'Montana'), (b'NA', b'National'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'NE', b'Nebraska'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NV', b'Nevada'), (b'NY', b'New York'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VA', b'Virginia'), (b'VI', b'Virgin Islands'), (b'VT', b'Vermont'), (b'WA', b'Washington'), (b'WI', b'Wisconsin'), (b'WV', b'West Virginia'), (b'WY', b'Wyoming')])),
                ('zipcd', models.IntegerField()),
                ('phone', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lng', models.FloatField(null=True, blank=True)),
                ('order', models.OneToOneField(related_name='address', to='members.AuthOrder')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('taxes', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, blank=None, help_text=b'Taxes in dollars', null=None)),
                ('original_price', models.DecimalField(default=0.0, help_text=b'Price of the product at the time of purchase', max_digits=8, decimal_places=2)),
                ('transaction_price', models.DecimalField(default=0.0, help_text=b'Total purchase price the user paid including promotions and taxes', max_digits=8, decimal_places=2)),
                ('authuser', models.ForeignKey(related_name='purchases', to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(related_name='purchase', to='members.AuthOrder')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Redemption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(help_text=b'When this was redeemed')),
                ('total_before_discount', models.DecimalField(decimal_places=2, default=None, max_digits=8, blank=True, help_text=b'Total dollar amount before applying any promotinal discounts to the order', null=True)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=None, max_digits=8, blank=True, help_text=b'Discount dollar amount', null=True)),
                ('authuser', models.ForeignKey(related_name='user_redemptions', to=settings.AUTH_USER_MODEL)),
                ('offer', models.ForeignKey(related_name='offer_redemptions', to='members.PromotionOffer')),
                ('order', models.ForeignKey(related_name='order_redemptions', to='members.AuthOrder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('reservation_price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('is_active', models.BooleanField(default=True)),
                ('reservation_expiration', models.DateTimeField()),
                ('authuser', models.ForeignKey(related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(related_name='reservation', to='members.AuthOrder')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='authuserorder',
            name='authuser',
        ),
        migrations.RemoveField(
            model_name='authuserorderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='authuserorderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='AuthUserOrderItem',
        ),
        migrations.RemoveField(
            model_name='promotionredemption',
            name='authuser',
        ),
        migrations.RemoveField(
            model_name='promotionredemption',
            name='offer',
        ),
        migrations.RemoveField(
            model_name='promotionredemption',
            name='order',
        ),
        migrations.DeleteModel(
            name='AuthUserOrder',
        ),
        migrations.DeleteModel(
            name='PromotionRedemption',
        ),
        migrations.RemoveField(
            model_name='authuseraddress',
            name='billing',
        ),
        migrations.RemoveField(
            model_name='authuseraddress',
            name='shipping',
        ),
        migrations.AlterField(
            model_name='authuseraddress',
            name='authuser',
            field=models.OneToOneField(related_name='default_address', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
