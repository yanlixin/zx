from flask import Flask, jsonify,abort,make_response,request,url_for
from flask_restful import Resource, Api,reqparse,fields
from flask_httpauth import HTTPBasicAuth
import os
from sqlalchemy import func,or_,cast,Numeric
from app import app, db, base_path
from app.models import Lecturer,LecturerGallery


class LecturerAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = int,default = -1, location='json')
        super(LecturerAPI, self).__init__()
    def post(self):
        args=self.reqparse.parse_args(strict=True)
        id = args['id']
        school=Lecturer.query.get(id)
        if school == None:
            return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})

        return jsonify({'msg':'','code':200,'data':school.to_dict()})

  

class LecturerListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, default = '', location='json')
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        self.reqparse.add_argument('sortname', type = str, default = '', location='json') #价格:tuition,默认:default
        self.reqparse.add_argument('sortorder', type = str, default = 'asc', location='json') # can only be 'asc' or 'desc'
        super(LecturerListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        name = args['name']
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        sortName=args['sortname']
        sortOrder=args['sortorder']
        query=Lecturer.query
        query=query.filter(or_(Lecturer.name.like('%'+name+'%'),Lecturer.title.like('%'+name+'%'),name==''))
        
        if sortName=="price":
            if sortOrder=='desc':
                query=query.order_by(Lecturer.price.desc())
            else:
                query=query.order_by(Lecturer.price.asc())
        else: 
            if sortOrder=='desc':
                query=query.order_by(Lecturer.sortindex.asc())
            else:
                query=query.order_by(Lecturer.sortindex.desc())

        #[item.to_dict() for item in 
       
        data=query.limit(pageSize).offset((pageIndex-1)*pageSize)
        data=[item.to_dict() for item in data]
        
        totalRow=db.session.query(func.count(Lecturer.id))\
        .filter(or_(Lecturer.name.like('%'+name+'%'),Lecturer.title.like('%'+name+'%'),name=='')).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})


class LecturerThumbAPI(Resource):
    def get(self,id):
        # Default to 200 OK
        #id = request.args.get('id', -1, type=int)
        obj = Lecturer.query.get(id)
        
        image_data = open(os.path.join(base_path, 'timg.jpg'), "rb").read()
        if obj.thumb is not None:
            image_data = open(''.join([base_path,  obj.thumb]), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response

class LecturerImgAPI(Resource):
    def get(self,t,id):
        # Default to 200 OK
        #id = request.args.get('id', -1, type=int)
        image_data=None
        if t=='n':
            obj=LecturerGallery.query.get(id)
            imagename = os.path.splitext(obj.path)
            origin = [base_path,r'/files/lecturers/',str(obj.objid),r'/',imagename[0],r'_origin_',imagename[1]]
            originname = ''.join(origin)
            image_data = open(os.path.join(base_path, originname), "rb").read()
        else:
            obj = Lecturer.query.get(id)
            image_data = open(os.path.join(base_path, 'timg.jpg'), "rb").read()

            if t=='s' and  obj.thumb is not None:
                image_data = open(''.join([base_path,  obj.thumb]), "rb").read()
            if t=='l' and  obj.img is not None:
                image_data = open(''.join([base_path,  obj.img]), "rb").read()
            if t=='a' and  obj.avatar is not None:
                image_data = open(''.join([base_path,  obj.avatar]), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
