from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import changeAppLogLevel

urlpatterns = [
    url(r'^changeloglevel$', changeAppLogLevel),
]