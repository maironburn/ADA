
from django.urls import path
from django.conf.urls import url
from .views import listRulefunction

app_name = 'rulefunction'
urlpatterns = [
    url(r'^rulefunction/$', listRulefunction),
]