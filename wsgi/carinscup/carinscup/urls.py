from django.conf.urls import url, include
from . import views

app_name = "cc"

cc_patterns = [
    url(r'^$', view=views.index, name='index'),
]

urlpatterns = [url(r'^', include(cc_patterns, namespace=app_name))]
