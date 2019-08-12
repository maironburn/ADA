
from django.urls import path
from django.conf.urls import url
from .views import listWorkflowMethodParameter

app_name = 'workflow_method_parameter'
urlpatterns = [
    url(r'^workflow_method_parameter/search/$', listWorkflowMethodParameter),
]