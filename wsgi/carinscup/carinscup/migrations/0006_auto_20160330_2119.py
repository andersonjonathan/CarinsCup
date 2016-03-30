# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0005_auto_20160330_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='course_length',
            field=models.CharField(max_length=255, verbose_name='banlängd', null=True, blank=True),
        ),
    ]
