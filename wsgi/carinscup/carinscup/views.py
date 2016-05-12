import collections

import datetime

import pytz as pytz
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Competitor, Event, Race, Result, Organisation
from eventor_toolkit import Eventor
from django.conf import settings


def index(request):
    year = timezone.now().year
    from_date = "{y}-02-15".format(y=year)
    to_date = "{y}-11-15".format(y=year)
    race_list = Race.objects.filter(event__start_date__gte=from_date, event__start_date__lte=to_date)
    cc = {}
    for r in race_list:
        for c in r.result_set.filter(points__isnull=False):
            if c.competitor.pk not in cc:
                cc[c.competitor.pk] = []
            cc[c.competitor.pk].append(c)
    tmp_sum = {}
    for key, val in cc.items():
        cc[key] = sorted(val, key=lambda x: x.points, reverse=True)
        if len(val) > 8:
            cc[key] = cc[key][0:8]
        tmp_sum[key] = sum(c.points for c in cc[key])
    tmp = collections.OrderedDict(sorted(cc.items(), key=lambda x: sum(c.points for c in x[1]), reverse=True))

    return render(request, 'carinscup/index.html', {"cc": tmp, 'sum': tmp_sum, 'choosen_year': year})


@xframe_options_exempt
def box(request):
    year = timezone.now().year
    from_date = "{y}-02-15".format(y=year)
    to_date = "{y}-11-15".format(y=year)
    race_list = Race.objects.filter(event__start_date__gte=from_date, event__start_date__lte=to_date)
    cc = {}
    for r in race_list:
        for c in r.result_set.filter(points__isnull=False):
            if c.competitor.pk not in cc:
                cc[c.competitor.pk] = []
            cc[c.competitor.pk].append(c)
    tmp_sum = {}
    for key, val in cc.items():
        cc[key] = sorted(val, key=lambda x: x.points, reverse=True)
        if len(val) > 8:
            cc[key] = cc[key][0:8]
        tmp_sum[key] = sum(c.points for c in cc[key])
    tmp = collections.OrderedDict(sorted(cc.items(), key=lambda x: sum(c.points for c in x[1]), reverse=True)[0:5])

    return render(request, 'carinscup/box.html', {"cc": tmp, 'sum': tmp_sum})


@xframe_options_exempt
def activities(request):
    e = Eventor(settings.API_KEY)
    tmp = e.activities(settings.ORGANISATION_ID, from_date=timezone.now())
    res = []
    if type(tmp) is not list:
        tmp = [tmp]
    for t in tmp:
        tmp_dict = {"name": t['Name']}
        try:
            tmp_dict["url"] = t['@url']
        except KeyError:
            pass
        try:
            tmp_dict["start_time"] = pytz.timezone('UTC').localize(
                timezone.datetime.strptime(t['@startTime'], "%Y-%m-%dT%H:%M:%SZ")
            ).astimezone(pytz.timezone('Europe/Stockholm'))
        except KeyError:
            pass
        try:
            tmp_dict["registration_deadline"] = pytz.timezone('UTC').localize(
                timezone.datetime.strptime(t['@registrationDeadline'], "%Y-%m-%dT%H:%M:%SZ")
            ).astimezone(pytz.timezone('Europe/Stockholm'))
        except KeyError:
            pass
        res.append(tmp_dict)
    return render(request, 'carinscup/activities.html',
                  {"activities": res})


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


def organisation(request, pk):
    tmp = get_object_or_404(Organisation, pk=pk)
    paginator = Paginator(tmp.event_set.all(), 20)

    page = request.GET.get('page')

    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    return render(request, 'carinscup/organisation.html', {"organisation": tmp, 'events': content})


def cc(request, year):
    from_date = "{y}-02-15".format(y=year)
    to_date = "{y}-11-15".format(y=year)
    race_list = Race.objects.filter(event__start_date__gte=from_date, event__start_date__lte=to_date)
    cc = {}
    for r in race_list:
        for c in r.result_set.filter(points__isnull=False):
            if c.competitor.pk not in cc:
                cc[c.competitor.pk] = []
            cc[c.competitor.pk].append(c)
    tmp_sum = {}
    for key, val in cc.items():
        cc[key] = sorted(val, key=lambda x: x.points, reverse=True)
        if len(val) > 8:
            cc[key] = cc[key][0:8]
        tmp_sum[key] = sum(c.points for c in cc[key])
    tmp = collections.OrderedDict(sorted(cc.items(), key=lambda x: sum(c.points for c in x[1]), reverse=True))

    return render(request, 'carinscup/cc.html', {"cc": tmp, 'sum': tmp_sum, 'choosen_year': year})

