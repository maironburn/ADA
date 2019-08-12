from django.urls import path
from django.conf.urls import url
from .views import validationscriptAction, modifyValidationscriptAction, reorder

app_name = 'validationscript'
urlpatterns = [
    url(r'^validationscript/$', validationscriptAction),
    url(r'^validationscript/(?P<pk>[0-9]+)/$', modifyValidationscriptAction),
    url(r'^validationscript/reorder/$', reorder)
]
