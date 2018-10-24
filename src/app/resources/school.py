from flask import Flask, jsonify,abort,make_response,request,url_for
from flask_restful import Resource, Api,reqparse,fields
from flask_httpauth import HTTPBasicAuth
import os
from sqlalchemy import func,or_,cast,Numeric
from app import app, db, base_path
from app.models import School,SchoolGallery,Province,City,District,Grade,Category,CBD
#api = Api(app)

# class SchoolAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('id', type = int,default = -1, location='json')
#         super(SchoolAPI, self).__init__()
#     def post(self):
#         args=self.reqparse.parse_args(strict=True)
#         id = args['id']
#         school=School.query.get(id)
#         if school == None:
#             return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})

#         return jsonify({'msg':'','code':200,'data':school.to_dict()})
        
# class SchoolAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('id', type = int,default = -1, location='json')
#         super(SchoolAPI, self).__init__()
#     def post(self):
#         args=self.reqparse.parse_args(strict=True)
#         id = args['id']
#         school=School.query.get(id)
#         if school == None:
#             return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})

#         return jsonify({'msg':'','code':200,'data':school.to_dict()})

class SchoolAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = int,default = -1, location='json')
        super(SchoolAPI, self).__init__()
    def post(self):
        args=self.reqparse.parse_args(strict=True)
        id = args['id']
        school=School.query.get(id)
        if school == None:
            return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})

        return jsonify({'msg':'','code':200,'data':school.to_dict()})

  

class SchoolListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('gradeid', type = int,default = -1, location='json')
        self.reqparse.add_argument('catid', type = int, default = -1, location='json')
        self.reqparse.add_argument('cityid', type = int, default = -1, location='json')
        self.reqparse.add_argument('distid', type = int, default = -1, location='json')
        self.reqparse.add_argument('cbdid', type = int, default = -1, location='json')
        self.reqparse.add_argument('isbilingual', type = int, default = -1, location='json')
        self.reqparse.add_argument('name', type = str, default = '', location='json')
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        self.reqparse.add_argument('tuition', type = str, default = '0~9999999', location='json') #tuition:0~1000
        self.reqparse.add_argument('sortname', type = str, default = '', location='json') #价格:tuition,默认:default
        self.reqparse.add_argument('sortorder', type = str, default = 'asc', location='json') # can only be 'asc' or 'desc'
        super(SchoolListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        
        gradeid = args['gradeid']
        catid = args['catid']
        cityid = args['cityid']
        distid = args['distid']
        cbdid = args['cbdid']
        isbilingual = args['isbilingual']
        name = args['name']
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        sortName=args['sortname']
        sortOrder=args['sortorder']
        tuition=args['tuition']
        tuitionList=str.split(tuition,'~') 
        print(tuitionList)
        tuitionB=tuitionList[0]
        tuitionE=tuitionList[1]
        query=School.query
        query=query.filter(or_(School.gradeid==gradeid,-1==gradeid))
        query=query.filter(or_(School.catid==catid,-1==catid))
        query=query.filter(or_(School.cityid==cityid,-1==cityid))
        query=query.filter(or_(School.districtid==distid,-1==distid))
        query=query.filter(or_(School.cbdid==cbdid,-1==cbdid))
        query=query.filter(or_(School.isbilingual==isbilingual,-1==isbilingual))
        query=query.filter(or_(cast(School.tuition,Numeric(12,2))>=tuitionB))
        query=query.filter(or_(cast(School.tuition,Numeric(12,2))<=tuitionE))
         
        query=query.filter(or_(School.name.like('%'+name+'%'),name==''))
        if sortName=="tuition":
            if sortOrder=='desc':
                query=query.order_by(School.tuition.desc())
            else:
                query=query.order_by(School.tuition.asc())
        else: 
            if sortOrder=='desc':
                query=query.order_by(School.sortindex.desc())
            else:
                query=query.order_by(School.sortindex.asc())

        #[item.to_dict() for item in 
       
        data=query.limit(pageSize).offset((pageIndex-1)*pageSize)
        data=[item.to_dict() for item in data]
        totalRow=db.session.query(func.count(School.id)).filter(or_(School.gradeid==gradeid,-1==gradeid))\
        .filter(or_(School.catid==catid,-1==catid))\
        .filter(or_(School.cityid==cityid,-1==cityid))\
        .filter(or_(School.districtid==distid,-1==distid))\
        .filter(or_(School.cbdid==cbdid,-1==cbdid))\
        .filter(or_(School.isbilingual==isbilingual,-1==isbilingual))\
        .filter(or_(cast(School.tuition,Numeric(12,2))>=tuitionB))\
        .filter(or_(cast(School.tuition,Numeric(12,2))<=tuitionE))\
        .filter(or_(School.name.like('%'+name+'%'),name=='')).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})


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
        print(t)
        image_data=None
        if t=='n':
            obj=SchoolGallery.query.get(id)
            imagename = os.path.splitext(obj.path)
            origin = [base_path,r'/files/schools/',str(obj.objid),r'/',imagename[0],r'_origin_',imagename[1]]
            originname = ''.join(origin)
            image_data = open(os.path.join(base_path, originname), "rb").read()
        else:
            school = School.query.get(id)
            
            image_data = open(os.path.join(base_path, 'timg.jpg'), "rb").read()

            if t=='s' and  school.thumb is not None:
                image_data = open(''.join([base_path,  school.thumb]), "rb").read()
            if t=='l' and  school.img is not None:
                image_data = open(''.join([base_path,  school.img]), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response

class ProvinceListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        super(ProvinceListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        
        
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        data=[item.to_dict() for item in Province.query.filter(1==1)
        .limit(pageSize).offset((pageIndex-1)*pageSize)]

        totalRow=db.session.query(func.count(Province.id)).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})
    
class CityListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('provid', type = int,default = -1, location='json')
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        super(CityListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        
        provId = args['provid']
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        data=[item.to_dict() for item in City.query.filter(or_(City.provid==provId,-1==provId))
        .limit(pageSize).offset((pageIndex-1)*pageSize)]

        totalRow=db.session.query(func.count(City.id)).filter(or_(City.provid==provId,-1==provId)).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})
    
class DistrictListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('cityid', type = int,default = -1, location='json')
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        super(DistrictListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        
        cityId = args['cityid']
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        data=[item.to_dict() for item in District.query.filter(or_(District.cityid==cityId,-1==cityId))
        .limit(pageSize).offset((pageIndex-1)*pageSize)]
        totalRow=db.session.query(func.count(District.id)).filter(or_(District.cityid==cityId,-1==cityId)).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})

class GradeListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        super(GradeListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        data=[item.to_mini_dict() for item in Grade.query.filter(1==1)
        .limit(pageSize).offset((pageIndex-1)*pageSize)]
        totalRow=db.session.query(func.count(Grade.id)).filter(1==1).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})


class CategoryListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('typeid', type = int, default = 1, location='json')
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        super(CategoryListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        typeid = args['typeid']
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        data=[item.to_mini_dict() for item in Category.query.filter(Category.typeid==typeid)
        .limit(pageSize).offset((pageIndex-1)*pageSize)]
        totalRow=db.session.query(func.count(Category.id)).filter(1==1).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})


class CBDListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        self.reqparse.add_argument('districtid', type = int,default = -1, location='json')
        super(CBDListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        districtid = args['districtid']
        pageIndex = args['pageindex']
        pageSize = args['pagesize']
        data=[item.to_dict() for item in CBD.query.filter(or_(CBD.districtid==districtid,-1==districtid))
        .limit(pageSize).offset((pageIndex-1)*pageSize)]
        totalRow=db.session.query(func.count(CBD.id)).filter(or_(CBD.districtid==districtid,-1==districtid)).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})
