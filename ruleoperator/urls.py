
from django.urls import path
from django.conf.urls import url
from .views import listRuleoperator

app_name = 'ruleoperator'
urlpatterns = [
    url(r'^ruleoperator/$', listRuleoperator),
]