import os
import settings
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

os.environ["HOME"] = settings.BITCOIN_HOME

app = Flask(__name__)
app.config["SITE_NAME"] = settings.SITE_NAME
app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['DEBUG'] = settings.DEBUG
db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
