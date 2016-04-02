from django.db import models
from .managers import CompetitorsManager, OrganisationManager
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


class Result(models.Model):
    competitor = models.ForeignKey(Competitor)
    race = models.ForeignKey(Race)
    course_length = models.CharField(verbose_name="banlängd", max_length=255, blank=True, null=True)
    class_name = models.CharField(verbose_name="klassnamn", max_length=255)
    nr_of_starts = models.IntegerField(verbose_name="antal startande", blank=True, null=True)
    position = models.CharField(verbose_name="placering", max_length=255, blank=True, null=True)
    time = models.CharField(verbose_name="tid", max_length=255, blank=True, null=True)
    time_diff = models.CharField(verbose_name="tid efter segraren", max_length=255, blank=True, null=True)
    status = models.CharField(verbose_name="status", max_length=255, blank=True, null=True)
    points = models.IntegerField(verbose_name='poäng', blank=True, null=True)

    class Meta:
        ordering = ['race__event__start_date']

    def __str__(self):
        """Return string representation of object"""
        return "{event}, {name}".format(event=self.race.event, name=self.competitor)