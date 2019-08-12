
import logging.config
import os
from django.conf import settings 


# Disable Django's logging setup
LOGGING_CONFIG = None


LOG_LEVEL = settings.LOG_LEVEL
LOG_FILE =  os.path.join(settings.LOG_DIR, settings.API_ENVIRONMENT+"_logfile.log")

#Add custom LOGGER_LEVEL AUDIT with highest priority
AUDIT_LEVEL_NUM = logging.CRITICAL
logging.addLevelName(AUDIT_LEVEL_NUM, "AUDIT")
def audit(self, message, *args, **kws):
    self._log(AUDIT_LEVEL_NUM, message, args, **kws) 
logging.Logger.audit = audit


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [%(process)d] [%(thread)d] %(message)s",
            'datefmt' : "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level':LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILE,
            'when': 'D', # daily, you can use 'midnight' as well
            'backupCount': 7, # 7 days backup
            'formatter': 'standard',
        },
        'console':{
            'level':LOG_LEVEL,
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers':['console', 'logfile'],
            'propagate': True,
            'level':LOG_LEVEL,
        },
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
       
    }
}

logging.config.dictConfig(LOGGING)
