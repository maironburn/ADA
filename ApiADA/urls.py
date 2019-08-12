"""ApiADA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(('changeloglevel.urls','changeloglevel'), namespace='changeloglevel')),
    url(r'^', include(('api_authentication.urls','api_authentication'), namespace='api_authentication')),
    url(r'^', include(('appparameter.urls','appparameter'), namespace='appparameter')),
    url(r'^', include(('workflow.urls','workflow'), namespace='workflow')),
    url(r'^', include(('workflow.workflow_method.urls','workflow.workflow_method'), namespace='workflow.workflow_method')),
    url(r'^', include(('workflow.workflow_method.workflow_method_parameter.urls','workflow.workflow_method.workflow_method_parameter'), namespace='workflow.workflow_method.workflow_method_parameter')),
    url(r'^', include(('workflow.workflow_script.urls','workflow.workflow_script'), namespace='workflow.workflow_script')),
    url(r'^', include(('kibana.urls','kibana'), namespace='kibana')),
    url(r'^', include(('pattern.urls','pattern'), namespace='pattern')),
    url(r'^', include(('ruleset.urls','ruleset'), namespace='ruleset')),
    url(r'^', include(('rule.urls','rule'), namespace='rule')),
    url(r'^', include(('condition.urls','condition'), namespace='condition')),
    url(r'^', include(('action.urls','action'), namespace='action')),
    url(r'^', include(('ruleoperator.urls','ruleoperator'), namespace='ruleoperator')),
    url(r'^', include(('rulefunction.urls','rulefunction'), namespace='rulefunction')),
    url(r'^', include(('rulesetfield.urls','rulesetfield'), namespace='rulesetfield')),
    url(r'^', include(('validationscript.urls','validationscript'), namespace='validationscript')),
    url(r'^', include(('elkquery.urls','elkquery'), namespace='elkquery')),
    url(r'^', include(('classification.urls','classification'), namespace='classification')),
    url(r'^', include(('auditprocess.urls','auditprocess'), namespace='auditprocess')),
    url(r'^', include(('analysiserror.urls','analysiserror'), namespace='analysiserror')),
    url(r'^', include(('tunnelssh.urls','tunnelssh'), namespace='tunnelssh')),

]
