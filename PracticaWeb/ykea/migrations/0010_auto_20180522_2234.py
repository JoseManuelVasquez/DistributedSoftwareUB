# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-22 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ykea', '0009_auto_20180522_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemquantity',
            name='id_itemquantity',
            field=models.AutoField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='linebill',
            name='id_linebill',
            field=models.AutoField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='linebill',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
