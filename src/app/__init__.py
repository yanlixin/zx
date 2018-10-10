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

from app.resources.user import RegistAPI,LoginAPI
from app.resources.task import TaskAPI,TaskListAPI
from app.resources.school import SchoolListAPI,ProvinceListAPI,CityListAPI,DistrictListAPI,GradeListAPI,CategoryListAPI,SchoolAPI,CBDListAPI
from app.resources.goods import GoodsCatAPI,GoodsCatListAPI

api = Api(app)

class SchoolThumbAPI(Resource):
    def get(self,id):
        # Default to 200 OK
        #id = request.args.get('id', -1, type=int)
        school = School.query.get(id)
        
        image_data = open(os.path.join(base_path, 'timg.jpg'), "rb").read()
        if school.thumb is not None:
            image_data = open(''.join([base_path,  school.thumb]), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response

class SchoolImgAPI(Resource):
    def get(self,t,id):
        # Default to 200 OK
        #id = request.args.get('id', -1, type=int)
        school = School.query.get(id)
        
        image_data = open(os.path.join(base_path, 'timg.jpg'), "rb").read()

        if t=='s' and  school.thumb is not None:
            image_data = open(''.join([base_path,  school.thumb]), "rb").read()
        if t=='l' and  school.img is not None:
            image_data = open(''.join([base_path,  school.img]), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
              
api.add_resource(TaskListAPI, '/api/v1.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/api/v1.0/task/<int:id>', endpoint = 'task')

api.add_resource(GoodsCatListAPI, '/api/v1.0/shop/cats', endpoint = 'shop_cats')
api.add_resource(GoodsCatAPI, '/api/v1.0/shop/cat', endpoint = 'shop_cat')
#api.add_resource(GoodsCatListAPI, '/shop/api/v1.0/goods/', endpoint = 'shop_cats')
#api.add_resource(TaskAPI, '/shop/api/v1.0/goods/<int:id>', endpoint = 'shop_cats')

api.add_resource(RegistAPI, '/api/v1.0/reg', endpoint = 'userreg')
api.add_resource(LoginAPI, '/api/v1.0/login', endpoint = 'userlogin')
api.add_resource(SchoolListAPI, '/api/v1.0/schools', endpoint = 'schools')

api.add_resource(SchoolAPI, '/api/v1.0/school', endpoint = 'school')

api.add_resource(ProvinceListAPI, '/api/v1.0/provs', endpoint = 'provs')
api.add_resource(CityListAPI, '/api/v1.0/cities', endpoint = 'cities')
api.add_resource(DistrictListAPI, '/api/v1.0/dists', endpoint = 'dists')
api.add_resource(CBDListAPI, '/api/v1.0/cbds', endpoint = 'cbds')
api.add_resource(GradeListAPI, '/api/v1.0/grades', endpoint = 'grades')
api.add_resource(CategoryListAPI, '/api/v1.0/cats', endpoint = 'cats')
#api.add_resource(SchoolThumbAPI, '/thumb/school/<int:id>', endpoint = 'thumb_school')
api.add_resource(SchoolImgAPI, '/img/school/<string:t>/<int:id>', endpoint = 'img_school')


