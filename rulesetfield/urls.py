
from django.urls import path
from django.conf.urls import url
from .views import rulesetfieldAction, modifyRulesetfieldAction, searchRulesetfield

app_name = 'rulesetfield'
urlpatterns = [
    url(r'^rulesetfield/$', rulesetfieldAction),
    url(r'^rulesetfield/(?P<pk>[0-9]+)/$', modifyRulesetfieldAction),
    url(r'^rulesetfield/search/$', searchRulesetfield),
]