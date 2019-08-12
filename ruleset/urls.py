from django.urls import path
from django.conf.urls import url
from .views import listRuleSet, updateRuleSet, searchRuleset, detailRuleSet, reorderRuleset

app_name = 'ruleset'
urlpatterns = [
    url(r'^ruleset/$', listRuleSet),
    url(r'^ruleset/(?P<pk>[0-9]+)/detail/$', detailRuleSet),
    url(r'^ruleset/(?P<pk>[0-9]+)/$', updateRuleSet),
    url(r'^ruleset/search/$', searchRuleset),
    url(r'^ruleset/(?P<pk>[0-9]+)/reorder/$', reorderRuleset),
]