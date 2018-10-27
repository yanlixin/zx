import os
from flask import Flask , jsonify,abort,make_response,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api,reqparse
from flask_cors import *
from flask_httpauth import HTTPBasicAuth

#base_path = '/Users/YanLixin/Documents/docker/zhexiao/admin/app' #0ee6b980-a140-11e8-a6eb-720005b306c0.jpg
#os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object('config')
base_path=app.config['PIC_PATH']
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from app.models import School

from app.resources.user import RegistAPI,LoginAPI,SmsAPI
from app.resources.task import TaskAPI,TaskListAPI
from app.resources.school import SchoolListAPI,SchoolThumbAPI,SchoolImgAPI
from app.resources.school import ProvinceListAPI,CityListAPI,DistrictListAPI,GradeListAPI,CategoryListAPI,SchoolAPI,CBDListAPI
from app.resources.goods import GoodsCatAPI,GoodsCatListAPI
from app.resources.show import ShowAPI,ShowListAPI,ShowThumbAPI,ShowImgAPI
from app.resources.lecturer import LecturerAPI,LecturerListAPI,LecturerImgAPI
from app.resources.training import TrainingAPI,TrainingListAPI,TrainingThumbAPI,TrainingImgAPI
from app.resources.trainingclass import TrainingClassAPI,TrainingClassListAPI,TrainingClassThumbAPI,TrainingClassImgAPI
api = Api(app)

              
api.add_resource(TaskListAPI, '/api/v1.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/api/v1.0/task/<int:id>', endpoint = 'task')

api.add_resource(GoodsCatListAPI, '/api/v1.0/shop/cats', endpoint = 'shop_cats')
api.add_resource(GoodsCatAPI, '/api/v1.0/shop/cat', endpoint = 'shop_cat')
#api.add_resource(GoodsCatListAPI, '/shop/api/v1.0/goods/', endpoint = 'shop_cats')
#api.add_resource(TaskAPI, '/shop/api/v1.0/goods/<int:id>', endpoint = 'shop_cats')

api.add_resource(RegistAPI, '/api/v1.0/reg', endpoint = 'userreg')
api.add_resource(LoginAPI, '/api/v1.0/login', endpoint = 'userlogin')
api.add_resource(SmsAPI, '/api/v1.0/sendsms', endpoint = 'sendsms')

api.add_resource(SchoolListAPI, '/api/v1.0/schools', endpoint = 'schools')

api.add_resource(SchoolAPI, '/api/v1.0/school', endpoint = 'school')

api.add_resource(ShowListAPI, '/api/v1.0/shows', endpoint = 'shows')
api.add_resource(ShowAPI, '/api/v1.0/show', endpoint = 'show')

api.add_resource(TrainingListAPI, '/api/v1.0/trainings', endpoint = 'trainings')
api.add_resource(TrainingAPI, '/api/v1.0/training', endpoint = 'training')

api.add_resource(TrainingClassListAPI, '/api/v1.0/classes', endpoint = 'classes')
api.add_resource(TrainingClassAPI, '/api/v1.0/class', endpoint = 'class')


api.add_resource(LecturerListAPI, '/api/v1.0/lecturers', endpoint = 'lecturers')
api.add_resource(LecturerAPI, '/api/v1.0/lecturer', endpoint = 'lecturer')

api.add_resource(ProvinceListAPI, '/api/v1.0/provs', endpoint = 'provs')
api.add_resource(CityListAPI, '/api/v1.0/cities', endpoint = 'cities')
api.add_resource(DistrictListAPI, '/api/v1.0/dists', endpoint = 'dists')
api.add_resource(CBDListAPI, '/api/v1.0/cbds', endpoint = 'cbds')
api.add_resource(GradeListAPI, '/api/v1.0/grades', endpoint = 'grades')
api.add_resource(CategoryListAPI, '/api/v1.0/cats', endpoint = 'cats')
#api.add_resource(SchoolThumbAPI, '/thumb/school/<int:id>', endpoint = 'thumb_school')
api.add_resource(SchoolImgAPI, '/img/school/<string:t>/<int:id>', endpoint = 'img_school')
api.add_resource(ShowImgAPI, '/img/show/<string:t>/<int:id>', endpoint = 'img_show')
api.add_resource(TrainingImgAPI, '/img/training/<string:t>/<int:id>', endpoint = 'img_training')
api.add_resource(TrainingClassImgAPI, '/img/class/<string:t>/<int:id>', endpoint = 'img_class')
api.add_resource(LecturerImgAPI, '/img/lecturer/<string:t>/<int:id>', endpoint = 'img_lecturer')


