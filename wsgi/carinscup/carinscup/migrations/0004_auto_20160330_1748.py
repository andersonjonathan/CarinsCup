# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carinscup', '0003_competitor_hidden'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('event_id', models.CharField(verbose_name='event id', unique=True, max_length=255)),
                ('name', models.CharField(verbose_name='tävlingsnamn', max_length=255)),
                ('event_form', models.CharField(verbose_name='tävlingsform', max_length=255)),
                ('event_status', models.IntegerField(verbose_name='eventstatuus')),
                ('classification', models.IntegerField(verbose_name='klassificering')),
                ('start_date', models.CharField(verbose_name='start datum', max_length=255)),
                ('end_date', models.CharField(verbose_name='slut datum', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('organisation_id', models.CharField(verbose_name='organisations id', unique=True, max_length=255)),
                ('name', models.CharField(verbose_name='namn', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('event_race_id', models.CharField(verbose_name='event race id', max_length=255)),
                ('name', models.CharField(verbose_name='racenamn', blank=True, max_length=255, null=True)),
                ('light_condition', models.CharField(verbose_name='ljusförhållanden', blank=True, max_length=255, null=True)),
                ('distance', models.CharField(verbose_name='racenamn', blank=True, max_length=255, null=True)),
                ('date', models.CharField(verbose_name='datum', blank=True, max_length=255, null=True)),
                ('event', models.ForeignKey(to='carinscup.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('course_length', models.CharField(verbose_name='banlängd', max_length=255)),
                ('class_name', models.CharField(verbose_name='klassnamn', max_length=255)),
                ('nr_of_starts', models.IntegerField(verbose_name='antal startande')),
                ('position', models.CharField(verbose_name='placering', blank=True, max_length=255, null=True)),
                ('time', models.CharField(verbose_name='tid', blank=True, max_length=255, null=True)),
                ('time_diff', models.CharField(verbose_name='tid efter segraren', blank=True, max_length=255, null=True)),
                ('status', models.CharField(verbose_name='status', blank=True, max_length=255, null=True)),
                ('points', models.IntegerField(verbose_name='poäng', null=True, blank=True)),
                ('competitor', models.ForeignKey(to='carinscup.Competitor')),
                ('event', models.ForeignKey(to='carinscup.Event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='organisations',
            field=models.ManyToManyField(to='carinscup.Organisation'),
        ),
    ]
