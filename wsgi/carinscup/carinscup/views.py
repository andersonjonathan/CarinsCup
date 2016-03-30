from pprint import pprint
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from eventor_toolkit import Eventor
from .models import Competitor, Event, Race, Result, Organisation


def index(request):

    members = "Hej"

    #members = e.members_in_organisation(settings.ORGANISATION_ID)

    return render(request, 'carinscup/index.html', {"organisation": members})


def competitors(request):
    return render(request, 'carinscup/competitors.html', {"users": Competitor.objects.all()})


def competitor(request, pk):
    user = get_object_or_404(Competitor, pk=pk)
    return render(request, 'carinscup/competitor.html', {"user": user})
