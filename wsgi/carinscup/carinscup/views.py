import collections
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Competitor, Event, Race, Result, Organisation


def index(request):
    year = timezone.now().year
    from_date = "{y}-02-15".format(y=year)
    to_date = "{y}-11-15".format(y=year)
    race_list = Race.objects.filter(event__start_date__gte=from_date, event__start_date__lte=to_date)
    cc = collections.OrderedDict()
    for r in race_list:
        for c in r.result_set.all():
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
    cc = collections.OrderedDict()
    for r in race_list:
        for c in r.result_set.all():
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

