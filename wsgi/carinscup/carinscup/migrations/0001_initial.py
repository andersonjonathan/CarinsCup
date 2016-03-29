# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('competitor_id', models.CharField(verbose_name='Eventor id', max_length=255)),
                ('given_name', models.CharField(verbose_name='förnamn', max_length=255)),
                ('family_name', models.CharField(verbose_name='efternamn', max_length=255)),
                ('sex', models.CharField(verbose_name='kön', max_length=255)),
                ('birth_date', models.CharField(verbose_name='födelsedatum', max_length=255)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
            ],
            options={
                'verbose_name': 'Medlemmar',
                'verbose_name_plural': 'Medlemmarna',
            },
        ),
    ]
