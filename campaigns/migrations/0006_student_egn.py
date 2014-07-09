# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_student_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='egn',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
