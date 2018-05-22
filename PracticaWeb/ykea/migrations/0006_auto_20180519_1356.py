# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-19 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ykea', '0005_auto_20180518_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='id_bill',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='itemquantity',
            name='id_itemquantity',
            field=models.AutoField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='linebill',
            name='id_linebill',
            field=models.AutoField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='id_shoppingcart',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
