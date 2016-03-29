# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='competitor_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='Eventor id'),
        ),
    ]
