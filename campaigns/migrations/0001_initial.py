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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(default='', max_length=40)),
                ('description', models.TextField(default='', max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(default='', max_length=10)),
                ('capacity', models.IntegerField(default=0)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign', default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('egn', models.CharField(default='', max_length=10)),
                ('entry_number', models.IntegerField(default=0)),
                ('first_name', models.CharField(default='', max_length=30)),
                ('second_name', models.CharField(default='', max_length=30)),
                ('third_name', models.CharField(default='', max_length=30)),
                ('address', models.CharField(default='', blank=True, max_length=50)),
                ('parent_name', models.CharField(default='', blank=True, max_length=100)),
                ('previous_school', models.CharField(default='', blank=True, max_length=100)),
                ('bel_school', models.FloatField(default=0, blank=True)),
                ('physics_school', models.FloatField(default=0, blank=True)),
                ('bel_exam', models.FloatField(default=0, blank=True)),
                ('maths_exam', models.FloatField(default=0, blank=True)),
                ('maths_tues_exam', models.FloatField(default=0, blank=True)),
                ('first_choice', models.CharField(default='', blank=True, max_length=2)),
                ('second_choice', models.CharField(default='', blank=True, max_length=2)),
                ('grades_evaluated', models.FloatField(default=0, blank=True)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign', default=1)),
                ('hall', models.ForeignKey(default=1, blank=True, to='campaigns.Hall')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
