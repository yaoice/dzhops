# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostlist',
            name='provision_state',
            field=models.CharField(max_length=60, verbose_name='provision_state', blank=True),
        ),
    ]
