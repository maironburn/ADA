
from django.urls import path
from django.conf.urls import url
from .views import listWorkflowMethod, execute, searchWorkflowMethod

app_name = 'workflow_method'
urlpatterns = [
    url(r'^workflow_method/$', listWorkflowMethod),
    url(r'^workflow_method/search/$', searchWorkflowMethod),
    url(r'^workflow_method/(?P<pk>[0-9]+)/execute/$', execute),
]