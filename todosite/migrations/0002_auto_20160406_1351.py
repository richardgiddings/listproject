# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-06 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todosite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]