from app.config import DebugConfig
from flask import Flask
from flask_login import LoginManager,current_user
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os 
#from flask_script import Manager, Shell

db = SQLAlchemy()
login_manager = LoginManager()
uploaded_photos = UploadSet()
base_path = os.path.dirname(os.path.abspath(__file__))
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('base','sys', 'forms', 'ui', 'home', 'tables', 'data', 'additional', 'base','zx'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    basicConfig(filename='error.log', level=DEBUG)
    logger = getLogger()
    logger.addHandler(StreamHandler())


def create_app(selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(DebugConfig)
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logs(app)
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.dirname(os.path.abspath(__file__))
    #app.config['UPLOADS_DEFAULT_URL'] = 'http://127.0.0.1:8000/uploads_images'
    app.config['UPLOADED_MYPIC_ALLOW'] = IMAGES
    uploaded_photos = UploadSet()
    configure_uploads(app, uploaded_photos)
    return app
