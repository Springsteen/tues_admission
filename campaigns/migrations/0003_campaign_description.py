# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_campaign_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='description',
            field=models.TextField(max_length=500, default=''),
            preserve_default=True,
        ),
    ]
