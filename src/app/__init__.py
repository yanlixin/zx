import os
from flask import Flask, jsonify,abort,make_response,request,url_for

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api,reqparse
from flask_cors import *

base_path = '/Users/YanLixin/Documents/docker/zhexiao/admin/app' #0ee6b980-a140-11e8-a6eb-720005b306c0.jpg
#os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object('config')
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
from app.resfulapi import TaskAPI,TaskListAPI,SchoolListAPI,ProvinceListAPI,CityListAPI,DistrictListAPI,GradeListAPI,CategoryListAPI,SchoolAPI
api = Api(app)
api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/task/<int:id>', endpoint = 'task')


api.add_resource(SchoolListAPI, '/api/v1.0/schools', endpoint = 'schools')

api.add_resource(SchoolAPI, '/api/v1.0/school', endpoint = 'school')

api.add_resource(ProvinceListAPI, '/api/v1.0/provs', endpoint = 'provs')
api.add_resource(CityListAPI, '/api/v1.0/cities', endpoint = 'cities')
api.add_resource(DistrictListAPI, '/api/v1.0/dists', endpoint = 'dists')
api.add_resource(GradeListAPI, '/api/v1.0/grades', endpoint = 'grades')
api.add_resource(CategoryListAPI, '/api/v1.0/cats', endpoint = 'cats')

