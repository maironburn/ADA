
from django.urls import path
from django.conf.urls import url
from .views import listWorkflowAuthorized

app_name = 'workflow'
urlpatterns = [
    url(r'^workflow/authorized/$', listWorkflowAuthorized),
]