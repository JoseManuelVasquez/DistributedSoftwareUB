# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-22 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ykea', '0006_auto_20180519_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='featured_photo',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_number',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='itemquantity',
            name='amountItem',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='linebill',
            name='quantity',
            field=models.CharField(max_length=10),
        ),
    ]
