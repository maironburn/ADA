
from django.urls import path
from django.conf.urls import url
from .views import listAnalysiserror, deleteAnalysiserror

app_name = 'analysiserror'
urlpatterns = [
    url(r'^analysiserror/$', listAnalysiserror),
    url(r'^analysiserror/(?P<pk>[0-9]+)/$', deleteAnalysiserror),
]