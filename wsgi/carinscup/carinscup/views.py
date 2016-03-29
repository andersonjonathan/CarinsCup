import os
from django.shortcuts import render
from eventor_toolkit import Eventor
API_KEY = str(os.environ.get('EVENTOR_API'))


def index(request):
    e = Eventor(API_KEY)
    return render(request, 'carinscup/index.html', {"organisation": dict(e.organisation_from_api_key()['Organisation'])})

