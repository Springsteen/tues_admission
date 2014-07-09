# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0007_auto_20140709_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='entry_number',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
