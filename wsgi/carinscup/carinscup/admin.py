from django.contrib import admin

from . import models

admin.site.register(models.Competitor)
admin.site.register(models.Organisation)

admin.site.register(models.Race)
admin.site.register(models.Event)
admin.site.register(models.Result)
