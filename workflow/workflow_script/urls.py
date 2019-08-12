
from django.urls import path
from django.conf.urls import url
from .views import listWorkflowScript

app_name = 'workflow_script'
urlpatterns = [
    url(r'^workflow_script/search/$', listWorkflowScript),
]