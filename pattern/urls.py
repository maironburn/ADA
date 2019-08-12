
from django.urls import path
from django.conf.urls import url
from .views import patternAction, modifyAction

app_name = 'pattern'
urlpatterns = [
    url(r'^pattern/$', patternAction),
    url(r'^pattern/(?P<pk>[0-9]+)/$', modifyAction),
]