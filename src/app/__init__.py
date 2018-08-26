import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

base_path = '/Users/YanLixin/Documents/docker/zhexiao/admin/app' #0ee6b980-a140-11e8-a6eb-720005b306c0.jpg
#os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
