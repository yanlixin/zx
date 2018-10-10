from flask import Flask, jsonify,abort,make_response,request,url_for
from flask_restful import Resource, Api,reqparse,fields
from flask_httpauth import HTTPBasicAuth

from sqlalchemy import func,or_
from app import app, db, base_path
from app.models import School,Province,City,District,Grade,Category,CBD
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
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
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
        data=[item.to_dict() for item in School.query.filter(or_(School.gradeid==gradeid,-1==gradeid))
        .filter(or_(School.catid==catid,-1==catid))
        .filter(or_(School.cityid==cityid,-1==cityid))
        .filter(or_(School.districtid==distid,-1==distid))
        .filter(or_(School.cbdid==cbdid,-1==cbdid))
        .filter(or_(School.isbilingual==isbilingual,-1==isbilingual))
        .filter(or_(School.name.like('%'+name+'%'),name==''))
        .limit(pageSize).offset((pageIndex-1)*pageSize)]

        totalRow=db.session.query(func.count(School.id)).filter(or_(School.gradeid==gradeid,-1==gradeid))\
        .filter(or_(School.catid==catid,-1==catid))\
        .filter(or_(School.cityid==cityid,-1==cityid))\
        .filter(or_(School.districtid==distid,-1==distid))\
        .filter(or_(School.cbdid==cbdid,-1==cbdid))\
        .filter(or_(School.isbilingual==isbilingual,-1==isbilingual))\
        .filter(or_(School.name.like('%'+name+'%'),name=='')).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})

class ProvinceListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
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
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
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
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
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
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
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
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
        super(CategoryListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        data=[item.to_mini_dict() for item in Category.query.filter(1==1)
        .limit(pageSize).offset((pageIndex-1)*pageSize)]
        totalRow=db.session.query(func.count(Category.id)).filter(1==1).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})


class CBDListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
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
