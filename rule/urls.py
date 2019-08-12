from django.urls import path
from django.conf.urls import url
from .views import actionRule, searchRules, searchRulesDetails, modifyRule, reorderRuleActions #, updateParameter, searchParameters

app_name = 'rule'
urlpatterns = [
    url(r'^rule/$', actionRule),
    url(r'^rule/search/$', searchRules),
    url(r'^rule/searchdetails/$', searchRulesDetails),
    url(r'^rule/(?P<pk>[0-9]+)/$', modifyRule),
    url(r'^rule/(?P<pk>[0-9]+)/reorderactions/', reorderRuleActions),
]
