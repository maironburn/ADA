"""
Django settings for foro project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import yaml
from core.utils.crypto import ADACrypto

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
API_ENVIRONMENT = os.environ.get('API_ENVIRONMENT', 'development')

print("Starting API for environment: " + API_ENVIRONMENT)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_DIR = os.path.join(BASE_DIR, 'config')

LOG_DIR = os.path.join(BASE_DIR, 'logs')

# we create a variable with the path our config application file
# with "yaml" library, we open application config file on read mode
application_config = yaml.safe_load(open(os.path.join(CONFIG_DIR, "application.yml"), "r"))
LOG_LEVEL = application_config[API_ENVIRONMENT]["LOG_LEVEL"]
DEFAULT_PWD = application_config[API_ENVIRONMENT]["DEFAULT_PWD"]
CERTS_FOLDER = os.path.join(BASE_DIR, application_config[API_ENVIRONMENT]["CERTS_FOLDER"])
DB_FOLDER = os.path.join(BASE_DIR, application_config[API_ENVIRONMENT]["DB_FOLDER"])
TMP_FOLDER = os.path.join(BASE_DIR, application_config[API_ENVIRONMENT]["TMP_FOLDER"])
PLINK_COMMAND = os.path.join(BASE_DIR, application_config[API_ENVIRONMENT]["PLINK_COMMAND"])

VALIDATION_SCRIPTS_PATH = application_config[API_ENVIRONMENT]["VALIDATION_SCRIPTS_PATH"]
VALIDATION_SCRIPTS_FOLDER = {}
for keyPath, valuePath in VALIDATION_SCRIPTS_PATH.items():
    tmpPath = os.path.abspath(BASE_DIR)
    pathItems = valuePath.split('.')
    for item in pathItems:
        tmpPath = os.path.join(tmpPath, item)

    VALIDATION_SCRIPTS_FOLDER[keyPath] = tmpPath

KIBANA_URL = application_config[API_ENVIRONMENT]["KIBANA_URL"]

# ELK VARIABLES
ELK_SERVER = application_config[API_ENVIRONMENT]["ELK_SERVER"]
ELK_PORT = application_config[API_ENVIRONMENT]["ELK_PORT"]
ELK_CERT = application_config[API_ENVIRONMENT]["ELK_CERT"]
ELK_CERT_KEY = application_config[API_ENVIRONMENT]["ELK_CERT_KEY"]
ELK_ROOT_CA = application_config[API_ENVIRONMENT]["ELK_ROOT_CA"]

# LOG_LEVEL = 'info'.upper()


permissions_config = yaml.safe_load(open(os.path.join(CONFIG_DIR, "permissions.yml"), "r"))
GROUPS_PRIORITY = permissions_config["info"]["groups_priority"]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = application_config[API_ENVIRONMENT]["SECRET_KEY"]
# SECRET_KEY = 'w1!&1sn!(s06boslk!-9vaydctd=fk9_40g_99-@zezi(6sw)$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = application_config[API_ENVIRONMENT]["DEBUG"]
# DEBUG = True

ALLOWED_HOSTS = []
ALLOWED_HOSTS = application_config[API_ENVIRONMENT]["ALLOWED_HOSTS"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework',
    'api_authentication',
    'changeloglevel',
    'tasks',
    'core',
    'appparameter',
    'kibana',
    'pattern',
    'ruleset',
    'rule',
    'condition',
    'ruleoperator',
    'rulesetfield',
    'analysiserror',
    'action',
    'rulefunction',
    'validationscript',
    'elkquery',
    'auditprocess',
    'clasification',
    'workflow',
    'workflow.workflow_method',
    'workflow.workflow_method.workflow_method_parameter',
    'workflow.workflow_script',
    'tokencontrol',
    'tunnelssh'

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api_authentication.backends.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'EXCEPTION_HANDLER': 'core.exceptions.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ApiADA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ApiADA.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

try:

    ## define custom tag handler
    def dbFolder(loader, node):
        seq = loader.construct_sequence(node)
        tmp = DB_FOLDER
        for i in seq:
            tmp = os.path.join(tmp, str(i))
        return tmp


    yaml.SafeLoader.add_constructor('!dbFolder', dbFolder)
    database_config = yaml.load(ADACrypto.decrypt_file(os.path.join(CONFIG_DIR, "databases.yml.crypt")),
                                Loader=yaml.SafeLoader)
    DATABASES = database_config[API_ENVIRONMENT]["databases"]

except Exception as e:
    print("WARNING. Unable to setup databases")

''' Sample of DATABASES variable
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'smart': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'kkkkkkkkkkkkkkkk',
        'USER': 'kkkk',
        'PASSWORD': 'kkkkkk',
    }
}
'''

DATABASE_ROUTERS = ['ApiADA.routers.ModelDatabaseRouter']

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

'''
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
'''

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'api_authentication.User'

# ldap variables
ldap_config = yaml.safe_load(open(os.path.join(CONFIG_DIR, "ldap.yml"), "r"))
LDAP_BASE_DN = ldap_config[API_ENVIRONMENT]["base_dn"]
LDAP_SERVER = ldap_config[API_ENVIRONMENT]["ldap_server"]
LDAP_ALLOWED_GROUPS = ldap_config[API_ENVIRONMENT]['allowed_groups']
LDAP_MAPPING_GROUPS = ldap_config[API_ENVIRONMENT]['mapping']

# CORS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False
try:
    CORS_ORIGIN_WHITELIST = application_config[API_ENVIRONMENT]["CORS_ORIGIN_WHITELIST"]
    print('CORS_ORIGIN_WHITELIST:' + ",".join(CORS_ORIGIN_WHITELIST))
except Exception as e:
    print('Unable to set CORS_ORIGIN_REGEX_WHITELIST')
    CORS_ORIGIN_WHITELIST = []

# ML
ML_FOLDER = os.path.join(BASE_DIR, application_config[API_ENVIRONMENT]["ML_FOLDER"])
ML_REDNEURONAL_FOLDER = os.path.join(ML_FOLDER, 'redneuronal')
ML_SVM_FOLDER = os.path.join(ML_FOLDER, 'svm')

try:
    from core.ml.redneuronal.mlRedNeuronal import MLredneuronal

    RED_NEURONAL_OBJECT = MLredneuronal(ML_FOLDER)
except Exception as e:
    print('WARNING NEURONAL NETWORK ML not loaded.')

try:
    from core.ml.SVM.mlSvm import MLsvm

    SVM_OBJECT = MLsvm(ML_FOLDER)
except Exception as e:
    print('WARNING SVM ML not loaded.')

print('SERVER startutp END')

