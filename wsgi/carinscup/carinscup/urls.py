from django.conf.urls import url, include
from . import views

app_name = "cc"

cc_patterns = [
    url(r'^$', view=views.index, name='index'),
    url(r'^box/$', view=views.box, name='box'),
    url(r'^activities/$', view=views.activities, name='activities'),
    url(r'^member/$', view=views.competitors, name='competitors'),
    url(r'^member/(?P<pk>[0-9]+)/$', view=views.competitor, name='competitor'),
    url(r'^about/$', view=views.about, name='about'),
    url(r'^event/$', view=views.events, name='events'),
    url(r'^event/(?P<pk>[0-9]+)/$', view=views.event, name='event'),
    url(r'^organisation/(?P<pk>[0-9]+)/$', view=views.organisation, name='organisation'),
    url(r'^cc/(?P<year>[0-9]+)/$', view=views.cc, name='cc'),
]

urlpatterns = [url(r'^', include(cc_patterns, namespace=app_name))]
