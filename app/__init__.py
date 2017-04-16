from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CsrfProtect
import os

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)
CsrfProtect(app)

app.config.from_object(os.environ['SEEDBASE_CONFIG'])


login_manager = LoginManager()
login_manager.init_app(app)

from app import models,api,views