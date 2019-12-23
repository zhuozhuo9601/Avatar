# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-12-23 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btitle', models.CharField(max_length=20, verbose_name='名称')),
                ('bpub_date', models.DateField(null=True, verbose_name='发布日期')),
                ('bread', models.IntegerField(default=0, verbose_name='阅读量')),
                ('bcomment', models.IntegerField(default=0, verbose_name='评论量')),
                ('image', models.ImageField(null=True, upload_to='booktest', verbose_name='图片')),
            ],
        ),
    ]