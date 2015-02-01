# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_registrationprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'e.g. First order 10% off', max_length=100)),
                ('short_terms', models.CharField(help_text=b'This is a short vertion of the terms that we can show to the user e.g. on a front page where they might actually read it.', max_length=1000)),
                ('terms', models.CharField(help_text=b'This is the "fine print", explaining in every details the terms of the promotion', max_length=10000)),
                ('limit_per_user', models.IntegerField(help_text=b'Positive number - how many times this offer can be used per user, -1 - unlimited')),
                ('is_active', models.BooleanField(default=False, help_text=b'This is On/Off switch for the offer')),
                ('offer_type', models.CharField(help_text=b'This field determines how offer is applied: e.g. "First order", or "$10 off towards next purchase', max_length=50, db_index=True, choices=[(b'FIRST_ORDER', b'First order')])),
                ('start_time', models.DateTimeField(default=None, help_text=b'When offer becomes available', null=True, blank=True)),
                ('end_time', models.DateTimeField(default=None, help_text=b'When offer expires', null=True, blank=True)),
                ('is_code_required', models.BooleanField(default=True)),
                ('code', models.CharField(default=b'', help_text=b'Code for the promotion. Codes are case insensitive, e.g. PROMO2015 and Promo2015 is the same thing, so cannot create two different codes like that.', max_length=100, db_index=True, blank=True)),
                ('discount_fixed_amount', models.DecimalField(decimal_places=2, default=None, max_digits=8, blank=True, help_text=b'e.g. $20 off', null=True)),
                ('discount_percent', models.DecimalField(decimal_places=4, default=None, max_digits=5, blank=True, help_text=b'Expressed as decimal fraction, e.g. value 0.1 is 10% off and 0.25 is 25% etc.', null=True)),
                ('discount_limit', models.DecimalField(decimal_places=2, default=None, max_digits=8, blank=True, help_text=b'Limits the Percent discount off to this value. This is applicable only when discount_percent is set', null=True)),
                ('is_discount', models.BooleanField(default=True, help_text=b'Is this offer containing a price discount? Some offer might not, e.g. Same day delivery is not a Discount kind of promition.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PromotionRedemption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(help_text=b'When this was redeemed')),
                ('total_before_discount', models.DecimalField(decimal_places=2, default=None, max_digits=8, blank=True, help_text=b'Total dollar amount before applying any promotinal discounts to the order', null=True)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=None, max_digits=8, blank=True, help_text=b'Discount dollar amount', null=True)),
                ('authuser', models.ForeignKey(related_name='user_redemptions', to=settings.AUTH_USER_MODEL)),
                ('offer', models.ForeignKey(related_name='offer_redemptions', to='members.PromotionOffer')),
                ('order', models.ForeignKey(related_name='order_redemptions', to='members.AuthUserOrder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
