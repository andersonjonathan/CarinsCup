from django.db import models
from .managers import CompetitorsManager
from django.utils import timezone
from django.core.urlresolvers import reverse


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
