
from django.urls import path
from django.conf.urls import url
from .views import executeTunnelSSH, actionTunnelSSH, modifyTunnelSSH

app_name = 'tunnelssh'
urlpatterns = [
    url(r'^tunnelssh/(?P<pk>[0-9]+)/execute/$', executeTunnelSSH),
    url(r'^tunnelssh/$', actionTunnelSSH),
    url(r'^tunnelssh/(?P<pk>[0-9]+)/$', modifyTunnelSSH),
]