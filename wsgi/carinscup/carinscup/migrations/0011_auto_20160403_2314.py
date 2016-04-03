# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0010_auto_20160403_0128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name_plural': 'Resulten', 'ordering': ['-race__event__start_date'], 'verbose_name': 'Resultat'},
        ),
    ]
