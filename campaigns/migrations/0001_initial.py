# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=40, default='')),
                ('description', models.TextField(max_length=500, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('egn', models.IntegerField(default=0)),
                ('entry_number', models.IntegerField(default=0)),
                ('first_name', models.CharField(max_length=30, default='')),
                ('second_name', models.CharField(max_length=30, default='')),
                ('third_name', models.CharField(max_length=30, default='')),
                ('address', models.CharField(blank=True, default='', max_length=50)),
                ('parent_name', models.CharField(blank=True, default='', max_length=100)),
                ('previous_school', models.CharField(blank=True, default='', max_length=100)),
                ('bel_school', models.FloatField(blank=True, default=0)),
                ('physics_school', models.FloatField(blank=True, default=0)),
                ('bel_exam', models.FloatField(blank=True, default=0)),
                ('maths_exam', models.FloatField(blank=True, default=0)),
                ('maths_tues_exam', models.FloatField(blank=True, default=0)),
                ('first_choice', models.CharField(blank=True, default='', max_length=2)),
                ('second_choice', models.CharField(blank=True, default='', max_length=2)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign', default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
