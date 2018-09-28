# from flask import Flask, jsonify,abort,make_response,request,url_for
# from flask_restful import Resource, Api,reqparse
# from flask_httpauth import HTTPBasicAuth

# from sqlalchemy import func,or_
# from app import app, db, lm,base_path
# from app.models import tasks,School,Province,City,District,Grade,Category,User
# #api = Api(app)
# auth = HTTPBasicAuth()
# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
    
#     print(username_or_token==None)
#     if username_or_token ==None or len(username_or_token)==0:
#         return False
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(loginname = username_or_token).first()
#         if not user or not user.check_password(password):
#             return False
#     #g.user = user
#     return True

# class LoginAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('loginname', type = str, required = True, location='json')
#         self.reqparse.add_argument('password', type = str, required = True, location='json')
#         super(LoginAPI, self).__init__()
#     def post(self):
#         args=self.reqparse.parse_args(strict=True)
#         loginname = args['loginname']
#         password = args['password']
#         user = User.query.filter_by(loginname=loginname).first()
#         if user is None :
#             return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})
#         if not user.check_password(password):
#             return jsonify({'msg':'USER_PWD_MISS','code':272,'data':None})
#         token=user.generate_auth_token()

#         return jsonify({'msg':'','code':200,'data':{ 'token': token.decode('ascii')}})

# class RegistAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('loginname', type = str, required = True, location='json')
#         self.reqparse.add_argument('password', type = str, required = True, location='json')
#         self.reqparse.add_argument('smscode', type = str, required = True, location='json')
#         super(RegistAPI, self).__init__()
#     def post(self):
#         args=self.reqparse.parse_args(strict=True)
#         loginname = args['loginname']
#         password = args['password']
#         smscode = args['smscode']
#         user=User.query.filter(User.loginname==loginname).first()
#         if user != None:
#             return jsonify({'msg':'USER_EXISTED','code':270,'data':None})
#         if smscode==None:
#             return jsonify({'msg':'SMS_CODE_MISS','code':271,'data':None})
#         user = User(loginname=loginname)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify({'msg':'OK','code':200,'data':{ 'username': user.loginname }})

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

  

# class SchoolListAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('gradeid', type = int,default = -1, location='json')
#         self.reqparse.add_argument('catid', type = int, default = -1, location='json')
#         self.reqparse.add_argument('distid', type = int, default = -1, location='json')
#         self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
#         self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
#         super(SchoolListAPI, self).__init__()

#     def post(self):
#         args=self.reqparse.parse_args()
        
#         gradeid = args['gradeid']
#         catid = args['catid']
#         distid = args['distid']
        
#         pageIndex = args['pageindex']
#         pageSize=args['pagesize']
#         data=[item.to_dict() for item in School.query.filter(or_(School.gradeid==gradeid,-1==gradeid))
#         .filter(or_(School.catid==catid,-1==catid))
#         .filter(or_(School.districtid==distid,-1==distid))
#         .limit(pageSize).offset((pageIndex-1)*pageSize)]

#         totalRow=db.session.query(func.count(School.id)).filter(or_(School.gradeid==gradeid,-1==gradeid)).filter(or_(School.catid==catid,-1==catid)).filter(or_(School.districtid==distid,-1==distid)).scalar()
#         totalPage=int(totalRow/pageSize)+1

#         return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})

# class ProvinceListAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
#         self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
#         super(ProvinceListAPI, self).__init__()

#     def post(self):
#         args=self.reqparse.parse_args()
        
        
#         pageIndex = args['pageindex']
#         pageSize=args['pagesize']
#         data=[item.to_dict() for item in Province.query.filter(1==1)
#         .limit(pageSize).offset((pageIndex-1)*pageSize)]

#         totalRow=db.session.query(func.count(Province.id)).scalar()
#         totalPage=int(totalRow/pageSize)+1

#         return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})
    
# class CityListAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('provid', type = int,default = -1, location='json')
#         self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
#         self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
#         super(CityListAPI, self).__init__()

#     def post(self):
#         args=self.reqparse.parse_args()
        
#         provId = args['provid']
#         pageIndex = args['pageindex']
#         pageSize=args['pagesize']
#         data=[item.to_dict() for item in City.query.filter(or_(City.provid==provId,-1==provId))
#         .limit(pageSize).offset((pageIndex-1)*pageSize)]

#         totalRow=db.session.query(func.count(City.id)).filter(or_(City.provid==provId,-1==provId)).scalar()
#         totalPage=int(totalRow/pageSize)+1

#         return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})
    
# class DistrictListAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('cityid', type = int,default = -1, location='json')
#         self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
#         self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
#         super(DistrictListAPI, self).__init__()

#     def post(self):
#         args=self.reqparse.parse_args()
        
#         cityId = args['cityid']
#         pageIndex = args['pageindex']
#         pageSize=args['pagesize']
#         data=[item.to_dict() for item in District.query.filter(or_(District.cityid==cityId,-1==cityId))
#         .limit(pageSize).offset((pageIndex-1)*pageSize)]
#         totalRow=db.session.query(func.count(District.id)).filter(or_(District.cityid==cityId,-1==cityId)).scalar()
#         totalPage=int(totalRow/pageSize)+1

#         return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})

# class GradeListAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
#         self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
#         super(GradeListAPI, self).__init__()

#     def post(self):
#         args=self.reqparse.parse_args()
        
#         pageIndex = args['pageindex']
#         pageSize=args['pagesize']
#         data=[item.to_mini_dict() for item in Grade.query.filter(1==1)
#         .limit(pageSize).offset((pageIndex-1)*pageSize)]
#         totalRow=db.session.query(func.count(Grade.id)).filter(1==1).scalar()
#         totalPage=int(totalRow/pageSize)+1

#         return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})


# class CategoryListAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('pageindex', type = int, default = 1, location='json')
#         self.reqparse.add_argument('pagesize', type = int, default = 10, location='json')
#         super(CategoryListAPI, self).__init__()

#     def post(self):
#         args=self.reqparse.parse_args()
        
#         pageIndex = args['pageindex']
#         pageSize=args['pagesize']
#         data=[item.to_mini_dict() for item in Category.query.filter(1==1)
#         .limit(pageSize).offset((pageIndex-1)*pageSize)]
#         totalRow=db.session.query(func.count(Category.id)).filter(1==1).scalar()
#         totalPage=int(totalRow/pageSize)+1

#         return jsonify({'msg':'','code':200,'data':{'page_number':pageIndex,'page_size':pageSize,'total_page':totalPage,'total_row':totalRow,'list': data}})


# class TaskListAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type = str, required = True,
#             help = 'No task title provided', location = 'json')
#         self.reqparse.add_argument('description', type = str, default = "", location = 'json')
#         super(TaskListAPI, self).__init__()
    
#     @auth.login_required
#     def get(self):
#         return jsonify({'tasks': tasks})

#     def post(self):
#         if not request.json or not 'title' in request.json:
#             abort(400)
#         task = {
#             'id': tasks[-1]['id'] + 1,
#             'title': request.json['title'],
#             'description': request.json.get('description', ""),
#             'done': False
#         }
#         tasks.append(task)
#         return jsonify({'task': task})

# class TaskAPI(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type = str, location = 'json')
#         self.reqparse.add_argument('description', type = str, location = 'json')
#         self.reqparse.add_argument('done', type = bool, location = 'json')
#         super(TaskAPI, self).__init__()
#     def get(self, id):
#         task = list(filter(lambda t: t['id'] == id, tasks))
#         if len(task) == 0:
#             abort(404)
#         return jsonify({'task': task[0]})

#     def put(self, id):
#         task = list(filter(lambda t: t['id'] == id, tasks))
#         if len(task) == 0:
#             abort(404)
#         task = tasks[0]
#         # args = self.reqparse.parse_args()
#         # for k, v in args.iteritems():
#         #     if v != None:
#         #         task[k] = v
#         return jsonify( { 'task': make_public_task(task) } )


#     def delete(self, id):
#         task = list(filter(lambda t: t['id'] == id, tasks)) 
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return jsonify({'result': True})

# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

# def make_public_task(task):
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task