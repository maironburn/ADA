
from django.urls import path
from django.conf.urls import url
from .views import elasticsearchqueryAction, modifyElasticsearchqueryAction,executeElasticsearchquery

app_name = 'elkquery'
urlpatterns = [
    url(r'^elasticsearch_query/$', elasticsearchqueryAction),
    url(r'^elasticsearch_query/(?P<pk>[0-9]+)/$', modifyElasticsearchqueryAction),
    url(r'^elasticsearch_query/execute/$', executeElasticsearchquery),
]