
from django.urls import path
from django.conf.urls import url
from .views import listAuditprocess, deleteAuditprocess

app_name = 'auditprocess'
urlpatterns = [
    url(r'^auditprocess/$', listAuditprocess),
    url(r'^auditprocess/(?P<pk>[0-9]+)/$', deleteAuditprocess),
]