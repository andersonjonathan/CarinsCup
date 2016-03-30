# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0004_auto_20160330_1748'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organisation',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='result',
            name='event',
        ),
        migrations.AddField(
            model_name='result',
            name='race',
            field=models.ForeignKey(to='carinscup.Race', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='race',
            name='distance',
            field=models.CharField(verbose_name='distans', max_length=255, blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='race',
            unique_together=set([('event', 'event_race_id')]),
        ),
    ]
