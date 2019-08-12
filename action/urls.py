
from django.urls import path
from django.conf.urls import url
from .views import actionAction, modifyAction, searchActions #, updateParameter, searchParameters

app_name = 'action'
urlpatterns = [
    #url(r'^action/$', listActions),
    url(r'^action/$', actionAction),
    url(r'^action/search/$', searchActions),
    url(r'^action/(?P<pk>[0-9]+)/$', modifyAction),
    #url(r'^appparameter/(?P<pk>[0-9]+)/$', updateParameter),
    #url(r'^appparameter/search/$', searchParameters),
]