import os
from dotenv import load_dotenv, find_dotenv

# Load dotenv for environment variables
load_dotenv(find_dotenv())

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY")

TEMPLATES_AUTO_RELOAD = True

WTF_CSRF_CHECK_DEFAULT = False

PSQL_USERNAME = "postgres"
PSQL_PASSWORD = "postgres"
PSQL_DATABASE = "test"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgres://'+PSQL_USERNAME+':'+PSQL_PASSWORD+'@localhost/' + PSQL_DATABASE