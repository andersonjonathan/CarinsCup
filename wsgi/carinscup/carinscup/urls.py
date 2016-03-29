from django.conf.urls import url, include
from . import views

app_name = "cc"

cc_patterns = [
    url(r'^$', view=views.index, name='index'),
    url(r'^member/$', view=views.competitors, name='competitors'),
    url(r'^member/(?P<pk>[0-9]+)/$', view=views.competitor, name='competitor')
]

urlpatterns = [url(r'^', include(cc_patterns, namespace=app_name))]
