# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0009_auto_20160403_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='class_points',
            field=models.IntegerField(null=True, blank=True, verbose_name='klass poäng'),
        ),
        migrations.AddField(
            model_name='result',
            name='time_diff_in_seconds',
            field=models.IntegerField(null=True, blank=True, verbose_name='poäng'),
        ),
        migrations.AddField(
            model_name='result',
            name='time_in_seconds',
            field=models.IntegerField(null=True, blank=True, verbose_name='poäng'),
        ),
        migrations.AddField(
            model_name='result',
            name='user_set_class_points',
            field=models.IntegerField(null=True, blank=True, verbose_name='användar definerad klass poäng'),
        ),
        migrations.AddField(
            model_name='result',
            name='user_set_nr_of_starts',
            field=models.IntegerField(null=True, blank=True, verbose_name='användar definerad antal startande'),
        ),
    ]
