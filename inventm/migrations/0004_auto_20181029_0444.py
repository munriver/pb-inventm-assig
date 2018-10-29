# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-29 04:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventm', '0003_auto_20181028_0334'),
    ]

    operations = [
        migrations.CreateModel(
            name='IrecordDel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='IrecordUnapproved',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('pname', models.CharField(max_length=20)),
                ('vendor', models.CharField(max_length=50)),
                ('mrp', models.IntegerField(default=0)),
                ('batch_num', models.IntegerField()),
                ('batch_date', models.DateField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='irecord',
            name='appr_status',
        ),
        migrations.AddField(
            model_name='irecordunapproved',
            name='edit_of',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventm.Irecord'),
        ),
        migrations.AddField(
            model_name='irecorddel',
            name='del_status_of',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventm.Irecord'),
        ),
    ]
