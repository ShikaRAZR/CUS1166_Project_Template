from flask import Flask, current_app

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

## from flask_migrate  import Migrate
## from flask_login import LoginManager

# Instanciate modules used in the project.

db = SQLAlchemy()

## migrate = Migrate()
## login = LoginManager()


def create_app(config_class=Config):

    app = Flask(__name__)

    # load configuration parameters from Config class
    app.config.from_object(config_class)

    # Initialize app for db and migrate modules.
    db.init_app(app)
    bootstrap = Bootstrap(app)
    ##migrate.init_app(app,db)
    ##login.init_app(app)


    # Added the autho blueprint
    ##from app.auth import bp as auth_routes_bp
    ##app.register_blueprint(auth_routes_bp,url_prefix='/auth')


    # Added the main app.
    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app;
