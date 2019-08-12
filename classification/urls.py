
from django.urls import path
from django.conf.urls import url
from .views import classificationAction

app_name = 'classification'
urlpatterns = [
    url(r'^averias_classification/$', classificationAction),
]