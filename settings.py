SITE_NAME = "Your Site Name"
BITCOIN_HOME = "/your/home/directory"
SECRET_KEY = "Some random string of letters and numbers."
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://username:password@localhost/database_name'
DEBUG = True # Set to False on production systems via settings_local.py.

# Override these settings with settings from settings_local, if such
# a module exists. (Makes updating live systems from Git easier.)
try:
    from settings_local import *
except ImportError:
    pass
