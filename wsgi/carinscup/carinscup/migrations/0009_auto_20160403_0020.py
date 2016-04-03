# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0008_auto_20160402_2207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name_plural': 'Resulten', 'verbose_name': 'Resultat', 'ordering': ['race__event__start_date']},
        ),
        migrations.AddField(
            model_name='result',
            name='created',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 4, 2, 22, 20, 18, 285723, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='modified',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 4, 2, 22, 20, 33, 380199, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
