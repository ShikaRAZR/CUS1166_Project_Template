# Imports the Blueprint class from flask.
from flask import Blueprint

bp = Blueprint('main',__name__)

from app.main import routes
