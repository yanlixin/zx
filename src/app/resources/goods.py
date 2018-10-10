from flask import Flask, jsonify,abort,make_response,request,url_for
from flask_restful import Resource, Api,reqparse
from flask_httpauth import HTTPBasicAuth

from sqlalchemy import func,or_
from app import app, db, base_path
from app.models import goods_cats
#api = Api(app)

# async def paging(page,pagesize,data):
#     if page <= 0:
#         page = 1
#     if page > int(len(data) / pagesize):
#         page = int(len(data) / pagesize) + 1
#     print(page)
#     start = (page - 1) * pagesize
#     end = page * pagesize
#     page_data = data[start:end]
#     return page_data
def paging(page,pagesize,data):
    if page <= 0:
        page = 1
    if page > int(len(data) / pagesize):
        page = int(len(data) / pagesize) + 1
    print(page)
    start = (page - 1) * pagesize
    end = page * pagesize
    page_data = data[start:end]
    return page_data

class GoodsCatAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = int,default = -1, location='json')
        super(GoodsCatAPI, self).__init__()
    def post(self):
        args=self.reqparse.parse_args(strict=True)
        id = args['id']
        data = list(filter(lambda t: t['id'] == id, goods_cats))
        
        if data == None:
            return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})

        return jsonify({'msg':'','code':200,'data':data})

  

class GoodsCatListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
        self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
        super(GoodsCatListAPI, self).__init__()

    def post(self):
        args=self.reqparse.parse_args()
       
        
        pageIndex = args['pageindex']
        pageSize=args['pagesize']
        # data=[item.to_dict() for item in School.query.filter(or_(School.catid==catid,-1==catid))
        # .limit(pageSize).offset((pageIndex-1)*pageSize)]

        # totalRow=db.session.query(func.count(School.id)).filter(or_(School.catid==catid,-1==catid)).scalar()
        data=paging(pageIndex,pageSize,goods_cats)
        totalRow=len(goods_cats)
        totalPage=int(totalRow/pageSize)+1
        
        return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})
