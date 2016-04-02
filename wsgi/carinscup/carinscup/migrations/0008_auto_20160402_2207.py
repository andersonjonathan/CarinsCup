# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0007_auto_20160330_2151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitor',
            options={'verbose_name_plural': 'Medlemmarna', 'verbose_name': 'Medlemmar', 'ordering': ['family_name', 'given_name']},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-start_date']},
        ),
        migrations.AlterModelOptions(
            name='race',
            options={'ordering': ['event__start_date']},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['race__event__start_date']},
        ),
        migrations.AlterField(
            model_name='result',
            name='position',
            field=models.IntegerField(blank=True, verbose_name='placering', null=True),
        ),
    ]
