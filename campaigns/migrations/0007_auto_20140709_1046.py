# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_student_egn'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='second_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='third_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=True,
        ),
    ]
