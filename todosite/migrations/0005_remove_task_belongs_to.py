# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-24 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todosite', '0004_task_belongs_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='belongs_to',
        ),
    ]
