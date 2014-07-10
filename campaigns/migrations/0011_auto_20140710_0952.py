# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0010_auto_20140709_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(default='', max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='bel_exam',
            field=models.FloatField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='bel_school',
            field=models.FloatField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='first_choice',
            field=models.CharField(default='', max_length=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='maths_exam',
            field=models.FloatField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='maths_tues_exam',
            field=models.FloatField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='parent_name',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='physics_school',
            field=models.FloatField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='previous_school',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='second_choice',
            field=models.CharField(default='', max_length=2, blank=True),
            preserve_default=True,
        ),
    ]
