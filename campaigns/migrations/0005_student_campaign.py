# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='campaign',
            field=models.ForeignKey(to='campaigns.Campaign', default=1),
            preserve_default=True,
        ),
    ]
