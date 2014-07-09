# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_student_entry_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
