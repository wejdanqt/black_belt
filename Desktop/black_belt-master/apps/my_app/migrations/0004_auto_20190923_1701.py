# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-23 14:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_auto_20190920_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('acount', models.CharField(max_length=255)),
                ('pos', models.FloatField()),
                ('neg', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='actived',
            new_name='active',
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='my_app.User'),
        ),
    ]
