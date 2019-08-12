activate_this = 'C:/ADA/ApiADA/env/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:\ADA\ApiADA\env\Lib\site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:\ADA\ApiADA')
sys.path.append('C:\ADA\ApiADA\ApiADA')
sys.path.append('C:\ADA\instantclient_18_5')
try:
   sys.path.remove('C:\oracle')
except Exception:
   pass
   
try:
   sys.path.remove('C:\oracle\bin')
except Exception:
   pass

os.environ['DJANGO_SETTINGS_MODULE'] = 'ApiADA.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ApiADA.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()