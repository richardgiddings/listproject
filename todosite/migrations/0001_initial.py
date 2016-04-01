# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-23 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(help_text='The title of the task.', max_length=20)),
                ('task_description', models.TextField(help_text='Enter a description for the task.', max_length=500)),
                ('task_due', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date due')),
            ],
        ),
    ]