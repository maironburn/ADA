from django.urls import path
from django.conf.urls import url
from .views import login, logout

app_name = 'api_authentication'
urlpatterns = [
    url(r'^login/?$', login),
    url(r'^logout/?$', logout),
]