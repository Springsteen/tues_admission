# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='grades_evaluated',
            field=models.FloatField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
