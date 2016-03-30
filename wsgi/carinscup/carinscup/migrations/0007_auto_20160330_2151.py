# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0006_auto_20160330_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='nr_of_starts',
            field=models.IntegerField(verbose_name='antal startande', blank=True, null=True),
        ),
    ]
