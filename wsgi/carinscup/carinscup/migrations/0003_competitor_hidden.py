# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0002_auto_20160329_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='dölj på sidan'),
        ),
    ]
