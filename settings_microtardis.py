from os import path
from tardis.settings_changeme import *

# Debug mode
DEBUG = False

# Test Runner Configuration
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Database settings
DATABASES = {}
DATABASES['default'] = {}
DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
DATABASES['default']['HOST'] = 'localhost'
DATABASES['default']['PORT'] = '3306'
DATABASES['default']['NAME'] = 'microtardis'
DATABASES['default']['USER'] = 'microtardis'
DATABASES['default']['PASSWORD'] = 'secret'

# Root URLs in MicroTardis
ROOT_URLCONF = 'tardis.microtardis.urls'

# extend template directory to TEMPLATE_DIRS
tmp = list(TEMPLATE_DIRS)
tmp.append(
    path.join(path.dirname(__file__),
    'microtardis/templates/').replace('\\', '/')
)
TEMPLATE_DIRS = tuple(tmp)

# Add Middleware
tmp = list(MIDDLEWARE_CLASSES)
tmp.append(
    'tardis.microtardis.filters.FilterInitMiddleware'
)
MIDDLEWARE_CLASSES = tuple(tmp)

# Post Save Filters
POST_SAVE_FILTERS = [
    ("tardis.microtardis.filters.exiftags.make_filter", ["MICROSCOPY_EXIF","http://exif.schema"]),
    ("tardis.microtardis.filters.spctags.make_filter", ["EDAXGenesis_SPC","http://spc.schema"]),
    ("tardis.microtardis.filters.dattags.make_filter", ["HKLEDSD_DAT","http://dat.schema"]),
    ]

# Log files
SYSTEM_LOG_FILENAME = '/var/www/html/mytardis/request.log'
MODULE_LOG_FILENAME = '/var/www/html/mytardis/tardis.log'

# Institution name
DEFAULT_INSTITUTION = "RMIT Microscopy and Microanalysis Facility"

# Directory path for image thumbnails
THUMBNAILS_PATH = path.abspath(path.join(path.dirname(__file__),
    '../var/thumbnails/')).replace('\\', '/')

# Installed application
INSTALLED_APPS = ("tardis.microtardis",) + INSTALLED_APPS

# Template loaders
TEMPLATE_LOADERS = (
    'tardis.microtardis.templates.loaders.app_specific.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

# Microtardis Media
MT_STATIC_URL_ROOT = '/static'
MT_STATIC_DOC_ROOT = path.join(path.dirname(__file__),
                               'microtardis/static').replace('\\', '/')

# smatplotlib module configuration                               
MATPLOTLIB_HOME = path.abspath(path.join(path.dirname(__file__), 
                                         '../')).replace('\\', '/')
# LDAP configuration
LDAP_USE_TLS = False
LDAP_URL = "ldap://localhost:38911/"
LDAP_USER_LOGIN_ATTR = "uid"
LDAP_USER_ATTR_MAP = {"givenName": "display", "mail": "email"}
LDAP_GROUP_ID_ATTR = "cn"
LDAP_GROUP_ATTR_MAP = {"description": "display"}
#LDAP_ADMIN_USER = ''
#LDAP_ADMIN_PASSWORD = ''
LDAP_BASE = 'dc=example, dc=com'
LDAP_USER_BASE = 'ou=People, ' + LDAP_BASE
LDAP_GROUP_BASE = 'ou=Group, ' + LDAP_BASE

# Priviate datafiles
PRIVATE_DATAFILES = False

# Staging Protocol
STAGING_PROTOCOL = 'localdb'
GET_FULL_STAGING_PATH_TEST = path.join(STAGING_PATH, "test_user")

# Filter middleware for auto-ingest
FILTER_MIDDLEWARE = (("tardis.microtardis.filters","FilterInitMiddleware"),)

# URL for EMBS authentication
EMBS_URL = "http://embs.rmit.edu.au/auth.php?"

# Staging Area and Data Store
#STAGING_PATH = '/directory/path/of/your/own/staging'
#FILE_STORE_PATH = '/directory/path/of/your/own/store'