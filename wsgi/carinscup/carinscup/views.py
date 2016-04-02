from pprint import pprint
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from eventor_toolkit import Eventor
from .models import Competitor, Event, Race, Result, Organisation


def index(request):

    members = "Hej"

    #members = e.members_in_organisation(settings.ORGANISATION_ID)

    return render(request, 'carinscup/index.html', {"organisation": members})


def about(request):
    return render(request, 'carinscup/about.html')


def competitors(request):
    return render(request, 'carinscup/competitors.html', {"users": Competitor.objects.all()})


def competitor(request, pk):
    user = get_object_or_404(Competitor, pk=pk)
    return render(request, 'carinscup/competitor.html', {"user": user})


def events(request):
    paginator = Paginator(Event.objects.all(), 20)

    page = request.GET.get('page')

    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    return render(request, 'carinscup/events.html', {"events": content})


def event(request, pk):
    tmp = get_object_or_404(Event, pk=pk)
    return render(request, 'carinscup/event.html', {"event": tmp})
