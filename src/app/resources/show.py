from flask import Flask, jsonify,abort,make_response,request,url_for
from flask_restful import Resource, Api,reqparse,fields
from flask_httpauth import HTTPBasicAuth

from sqlalchemy import func,or_,cast,Numeric
from app import app, db, base_path
from app.models import Show,Province,City,District,Grade,Category,CBD
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

class ShowAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = int,default = -1, location='json')
        super(ShowAPI, self).__init__()
    def post(self):
        args=self.reqparse.parse_args(strict=True)
        id = args['id']
        school=Show.query.get(id)
        if school == None:
            return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})

        return jsonify({'msg':'','code':200,'data':school.to_dict()})

  

class ShowListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('catid', type = int, default = -1, location='json')
        self.reqparse.add_argument('cityid', type = int, default = -1, location='json')
        self.reqparse.add_argument('distid', type = int, default = -1, location='json')
        self.reqparse.add_argument('cbdid', type = int, default = -1, location='json')
        self.reqparse.add_argument('name', type = str, default = '', location='json')
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 1000, location='json')
        self.reqparse.add_argument('price', type = str, default = '0~9999999', location='json') #tuition:0~1000
        self.reqparse.add_argument('sortname', type = str, default = '', location='json') #价格:tuition,默认:default
        self.reqparse.add_argument('sortorder', type = str, default = 'asc', location='json') # can only be 'asc' or 'desc'
        super(ShowListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
        catid = args['catid']
        cityid = args['cityid']
        distid = args['distid']
        cbdid = args['cbdid']
        name = args['name']
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        sortName=args['sortname']
        sortOrder=args['sortorder']
        tuition=args['price']
        tuitionList=str.split(tuition,'~') 
        print(tuitionList)
        tuitionB=tuitionList[0]
        tuitionE=tuitionList[1]
        query=Show.query
        query=query.filter(or_(Show.catid==catid,-1==catid))
        query=query.filter(or_(Show.cityid==cityid,-1==cityid))
        query=query.filter(or_(Show.districtid==distid,-1==distid))
        query=query.filter(or_(Show.cbdid==cbdid,-1==cbdid))
        query=query.filter(or_(cast(Show.price,Numeric(12,2))>=tuitionB))
        query=query.filter(or_(cast(Show.price,Numeric(12,2))<=tuitionE))
         
        query=query.filter(or_(Show.name.like('%'+name+'%'),name==''))
        if sortName=="price":
            if sortOrder=='desc':
                query=query.order_by(Show.price.desc())
            else:
                query=query.order_by(Show.price.asc())
        else: 
            if sortOrder=='desc':
                query=query.order_by(Show.sortindex.desc())
            else:
                query=query.order_by(Show.sortindex.asc())

        #[item.to_dict() for item in 
       
        data=query.limit(pageSize).offset((pageIndex-1)*pageSize)
        data=[item.to_dict() for item in data]
        
        totalRow=db.session.query(func.count(Show.id))\
        .filter(or_(Show.catid==catid,-1==catid))\
        .filter(or_(Show.cityid==cityid,-1==cityid))\
        .filter(or_(Show.districtid==distid,-1==distid))\
        .filter(or_(Show.cbdid==cbdid,-1==cbdid))\
        .filter(or_(cast(Show.price,Numeric(12,2))>=tuitionB))\
        .filter(or_(cast(Show.price,Numeric(12,2))<=tuitionE))\
        .filter(or_(Show.name.like('%'+name+'%'),name=='')).scalar()
        totalPage=int(totalRow/pageSize)+1

        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})
