from tardis.test_settings import *

# --------------------------------------
# -- MicroTardis settings for testing --
# --------------------------------------

# Add Middleware
tmp = list(MIDDLEWARE_CLASSES)
tmp.append(
    'tardis.microtardis.filters.FilterInitMiddleware'
)
MIDDLEWARE_CLASSES = tuple(tmp)

# Post Save Filters
POST_SAVE_FILTERS = [
    ("tardis.microtardis.filters.exiftags.make_filter", ["MICROSCOPY_EXIF","http://rmmf.isis.rmit.edu.au/schemas"]),
    ("tardis.microtardis.filters.spctags.make_filter", ["EDAXGenesis_SPC","http://rmmf.isis.rmit.edu.au/schemas"]),
    ("tardis.microtardis.filters.dattags.make_filter", ["HKLEDSD_DAT","http://rmmf.isis.rmit.edu.au/schemas"]),
    ]

# Directory path for image thumbnails
THUMBNAILS_PATH = path.abspath(path.join(path.dirname(__file__),
    '../var/thumbnails/')).replace('\\', '/')

# Microtardis Media
MT_STATIC_URL_ROOT = '/static'
MT_STATIC_DOC_ROOT = path.join(path.dirname(__file__),
                               'microtardis/static').replace('\\', '/')

# smatplotlib module configuration                               
MATPLOTLIB_HOME = path.abspath(path.join(path.dirname(__file__), 
                                         '../')).replace('\\', '/')


# Staging Protocol
STAGING_PROTOCOL = 'localdb'
GET_FULL_STAGING_PATH_TEST = path.join(STAGING_PATH, "test_user")

# Filter middleware for auto-ingest
FILTER_MIDDLEWARE = (("tardis.microtardis.filters","FilterInitMiddleware"),)

# URL for EMBS authentication
EMBS_URL = "http://embs.rmit.edu.au/auth.php?"