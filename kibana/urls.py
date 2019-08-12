
from django.urls import path
from django.conf.urls import url
from .views import getUrl

app_name = 'kibana'
urlpatterns = [
    url(r'^kibana/$', getUrl)
]