import collections
import re
import time
from django.db import models
from django.db.models import Count

from .managers import CompetitorsManager, OrganisationManager, ResultsManager
from django.utils import timezone
from django.core.urlresolvers import reverse
from eventor_toolkit import Eventor


class Competitor(models.Model):
    competitor_id = models.CharField(
        unique=True,
        verbose_name="Eventor id",
        max_length=255)
    given_name = models.CharField(
        verbose_name="förnamn",
        max_length=255)
    family_name = models.CharField(
        verbose_name="efternamn",
        max_length=255)
    sex = models.CharField(
        verbose_name="kön",
        max_length=255)
    birth_date = models.CharField(
        verbose_name="födelsedatum",
        max_length=255)
    hidden = models.BooleanField(verbose_name="dölj på sidan", default=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    objects = CompetitorsManager()

    class Meta:
        verbose_name = "Medlemmar"
        verbose_name_plural = "Medlemmarna"
        ordering = ['family_name', 'given_name']

    def save(self, *args, **kwargs):
        """Override save to set created and modifed date before saving."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Competitor, self).save(*args, **kwargs)

    def __str__(self):
        """Return string representation of object"""
        return "{given} {family}".format(given=self.given_name, family=self.family_name)

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('cc:competitor', kwargs={'pk': self.pk})


class Organisation(models.Model):
    organisation_id = models.CharField(unique=True, verbose_name="organisations id", max_length=255)
    name = models.CharField(verbose_name="namn", max_length=255)
    objects = OrganisationManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Return string representation of object"""
        return self.name

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('cc:organisation', kwargs={'pk': self.pk})


class Event(models.Model):
    event_id = models.CharField(unique=True, verbose_name="event id", max_length=255)
    name = models.CharField(verbose_name="tävlingsnamn", max_length=255)
    event_form = models.CharField(verbose_name="tävlingsform", max_length=255)
    event_status = models.IntegerField(verbose_name="eventstatuus")
    classification = models.IntegerField(verbose_name="klassificering")
    start_date = models.CharField(verbose_name="start datum", max_length=255)
    end_date = models.CharField(verbose_name="slut datum", max_length=255)
    organisations = models.ManyToManyField(Organisation)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        """Return string representation of object"""
        return self.name

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('cc:event', kwargs={'pk': self.pk})

    def runners(self):
        res = Result.objects.none()
        for r in self.race_set.all():
            res |= r.result_set.all()
        return res.values_list('competitor').distinct()

    def results(self):
        res = Result.objects.none()
        for r in self.race_set.all():
            res |= r.result_set.all()
        return res.distinct()

    def event_form_hr(self):

        try:
            tmp = Eventor.EVENT_FORM_MAPPING[self.event_form]
        except:
            tmp = self.event_form
        return tmp

    def event_status_hr(self):

        try:
            tmp = Eventor.EVENT_STATUS_ID_MAPPING[self.event_status]
        except:
            tmp = self.event_status
        return tmp

    def classification_hr(self):
        try:
            tmp = Eventor.CLASSIFICATION_ID_MAPPING[self.classification]
        except:
            tmp = self.classification
        return tmp


class Race(models.Model):
    event = models.ForeignKey(Event)
    event_race_id = models.CharField(verbose_name="event race id", max_length=255)
    name = models.CharField(verbose_name="racenamn", max_length=255, blank=True, null=True)
    light_condition = models.CharField(verbose_name="ljusförhållanden", max_length=255, blank=True, null=True)
    distance = models.CharField(verbose_name="distans", max_length=255, blank=True, null=True)
    date = models.CharField(verbose_name="datum", max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('event', 'event_race_id')
        ordering = ['event__start_date']

    def __str__(self):
        """Return string representation of object"""
        if self.name:
            return self.name
        return str(self.event)

    def light_condition_hr(self):
        mapping = {'Day': 'dag',
                   'Night': 'natt'}
        try:
            tmp = mapping[self.light_condition]
        except:
            tmp = self.light_condition
        return tmp

    def distance_hr(self):
        mapping = {'Long': 'lång',
                   'Middle': 'medel',
                   'Sprint': 'sprint'}
        try:
            tmp = mapping[self.distance]
        except:
            tmp = self.distance
        return tmp

    def runners(self):
        res = self.result_set.all()
        return res.values_list('competitor').distinct()

    def results(self):
        res = self.result_set.all().annotate(
            null_position=Count('position')).order_by('class_name', '-null_position', 'position')
        prev = None
        res_dict = collections.OrderedDict()
        for r in res:
            if r.class_name != prev:
                prev = r.class_name
                res_dict[r.class_name] = [r]
            else:
                res_dict[r.class_name].append(r)
        return res_dict


class Result(models.Model):
    competitor = models.ForeignKey(Competitor)
    race = models.ForeignKey(Race)
    course_length = models.CharField(verbose_name="banlängd", max_length=255, blank=True, null=True)
    class_name = models.CharField(verbose_name="klassnamn", max_length=255)
    nr_of_starts = models.IntegerField(verbose_name="antal startande", blank=True, null=True)
    user_set_nr_of_starts = models.IntegerField(verbose_name="användar definerad antal startande", blank=True, null=True)
    position = models.IntegerField(verbose_name="placering", blank=True, null=True)
    time = models.CharField(verbose_name="tid", max_length=255, blank=True, null=True)
    time_diff = models.CharField(verbose_name="tid efter segraren", max_length=255, blank=True, null=True)
    status = models.CharField(verbose_name="status", max_length=255, blank=True, null=True)
    points = models.IntegerField(verbose_name='poäng', blank=True, null=True)
    class_points = models.IntegerField(verbose_name='klass poäng', blank=True, null=True)
    user_set_class_points = models.IntegerField(verbose_name='användar definerad klass poäng', blank=True, null=True)
    time_in_seconds = models.IntegerField(verbose_name='poäng', blank=True, null=True)
    time_diff_in_seconds = models.IntegerField(verbose_name='poäng', blank=True, null=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    objects = ResultsManager()

    class Meta:
        verbose_name = "Resultat"
        verbose_name_plural = "Resulten"
        ordering = ['-race__event__start_date']

    def save(self, *args, **kwargs):
        """Override save to set created and modifed date before saving."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Result, self).save(*args, **kwargs)

    def __str__(self):
        """Return string representation of object"""
        return "{event}, {name}".format(event=self.race.event, name=self.competitor)

    def course_length_hr(self):
        if self.course_length:
            try:
                if float(self.course_length) == 0:
                    return None
                return "{length} m".format(length=float(self.course_length))
            except:
                return self.course_length
        else:
            return None

    def speed(self):
        if self.course_length:
            try:
                if float(self.course_length) == 0:
                    return None
                length = float(self.course_length)
            except:
                try:
                    length = float(re.findall("[-+]?\d+[\.]?\d*", self.course_length))
                except:
                    return None
        if not self.time_in_seconds or self.time_in_seconds == 0:
            return None
        try:
            sp = float((self.time_in_seconds * 100)/(length * 6))
        except:
            return None

        return "{m}:{s}".format(m=int(sp), s=round((sp - int(sp))*60))

    def parse_cc_points(self):
        try:
            time_min, time_sec = self.time.split(':')
            self.time_in_seconds = int(time_min) * 60 + int(time_sec)
            if self.time_in_seconds == 0:
                self.time_in_seconds = None
        except:
            pass
        try:
            diff_min, diff_sec = self.time_diff.split(':')
            self.time_diff_in_seconds = int(diff_min) * 60 + int(diff_sec)
        except:
            pass

        self.class_points = self._get_class_points()
        self.save()
        self.calculate_cc_points()

    def calculate_cc_points(self):
        if self.status.upper() == "OK":
            if self.user_set_class_points:
                class_points = self.user_set_class_points
            else:
                class_points = self.class_points
            try:
                winner_time = self.time_in_seconds-self.time_diff_in_seconds
            except:
                self.points = 0
                self.save()
                return None
            points = (winner_time/self.time_in_seconds)*class_points + self._get_additional_points()
            if points < 50:
                points = 50
            self.points = round(points)
        else:
            self.points = 0
        self.save()

    def _get_additional_points(self):
        if self.user_set_nr_of_starts:
            nr_of_starts = self.user_set_nr_of_starts
        else:
            nr_of_starts = self.nr_of_starts
        if not nr_of_starts:
            return 0
        if nr_of_starts < 3:
            return 0
        elif nr_of_starts < 6:
            return 1
        elif nr_of_starts < 10:
            return 2
        elif nr_of_starts < 16:
            return 3
        elif nr_of_starts < 25:
            return 4
        else:
            return 5

    def _get_class_points(self):
        if 'B' == self.class_name.upper()[0]:  # Uppvidinge Karusell
            return 75
        if 'Ö' == self.class_name.upper()[0] or 'O' == self.class_name.upper()[0]:  # Öppen/Open
            return 75
        if 'U' == self.class_name.upper()[0]:  # U-klass
            return 80
        if 'I' == self.class_name.upper()[0]:  # Inskolning
            return 50
        if 'SSM' in self.class_name.upper():  # SSM
            return 97
        if 'SM' in self.class_name.upper():  # SM
            return 100
        if 'GM' in self.class_name.upper():  # GM
            return 98
        if 'DM' in self.class_name.upper():  # DM
            return 94
        if self.race.event.classification == 1:  # Championship, at least on district level
            return 94
        if 'M' in self.class_name.upper():  # Motion
            return 80
        if 'K' in self.class_name.upper():  # Kort
            return 85
        if 'L' in self.class_name.upper():  # Lång
            return 92
        if 'E' in self.class_name.upper():  # Elit
            return 95
        return 90  # Huvudklass


