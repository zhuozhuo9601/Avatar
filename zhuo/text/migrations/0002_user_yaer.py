# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-11-15 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='yaer',
            field=models.CharField(max_length=11, null=True, verbose_name='年龄'),
        ),
    ]
