# Get access to the os .
import os

# Get the absolute path of the current file.
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # flask-SQLAlchemy extension takes the location of the
    # application's database from the SQLALCHEMY_DATABASE_URI configuration variable.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir,'app.db')

    # Disable Track notifications feature from Flask-SQLAlchemy

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key-for-cus1166'
