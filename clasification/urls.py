
from django.urls import path
from django.conf.urls import url
from .views import clasificationAction, modifyClasificationAction

app_name = 'clasification'
urlpatterns = [
    url(r'^averias_clasification/$', clasificationAction),
    url(r'^averias_clasification/(?P<pk>[0-9]+)/$', modifyClasificationAction),
]