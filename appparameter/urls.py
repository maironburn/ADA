
from django.urls import path
from django.conf.urls import url
from .views import listParameters, updateParameter, searchParameters

app_name = 'appparameter'
urlpatterns = [
    url(r'^appparameter/$', listParameters),
    url(r'^appparameter/(?P<pk>[0-9]+)/$', updateParameter),
    url(r'^appparameter/search/$', searchParameters),
]