
from django.urls import path
from django.conf.urls import url
from .views import conditionAction, modifyConditionAction

app_name = 'condition'
urlpatterns = [
    url(r'^condition/$', conditionAction),
    url(r'^condition/(?P<pk>[0-9]+)/$', modifyConditionAction),
]