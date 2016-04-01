# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-24 13:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todosite', '0003_remove_task_belongs_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='belongs_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]