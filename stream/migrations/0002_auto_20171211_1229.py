# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-11 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'stream_tracks',
            },
        ),
        migrations.AlterField(
            model_name='streamuser',
            name='stream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='stream.Stream'),
        ),
    ]
