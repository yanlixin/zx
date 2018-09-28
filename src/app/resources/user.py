from flask import Flask, jsonify,abort,make_response,request,url_for
from flask_restful import Resource, Api,reqparse

from sqlalchemy import func,or_
from app.models import User
#api = Api(app)
from app import db,auth
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    
    print(username_or_token==None)
    if username_or_token ==None or len(username_or_token)==0:
        return False
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(loginname = username_or_token).first()
        if not user or not user.check_password(password):
            return False
    #g.user = user
    return True

class LoginAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('loginname', type = str, required = True, location='json')
        self.reqparse.add_argument('password', type = str, required = True, location='json')
        super(LoginAPI, self).__init__()
    def post(self):
        args=self.reqparse.parse_args(strict=True)
        loginname = args['loginname']
        password = args['password']
        user = User.query.filter_by(loginname=loginname).first()
        if user is None :
            return jsonify({'msg':'NO_DATA_FOUND','code':201,'data':None})
        if not user.check_password(password):
            return jsonify({'msg':'USER_PWD_MISS','code':272,'data':None})
        token=user.generate_auth_token()

        return jsonify({'msg':'','code':200,'data':{ 'token': token.decode('ascii')}})

class RegistAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('loginname', type = str, required = True, location='json')
        self.reqparse.add_argument('password', type = str, required = True, location='json')
        self.reqparse.add_argument('smscode', type = str, required = True, location='json')
        super(RegistAPI, self).__init__()
    def post(self):
        args=self.reqparse.parse_args(strict=True)
        loginname = args['loginname']
        password = args['password']
        smscode = args['smscode']
        user=User.query.filter(User.loginname==loginname).first()
        if user != None:
            return jsonify({'msg':'USER_EXISTED','code':270,'data':None})
        if smscode==None:
            return jsonify({'msg':'SMS_CODE_MISS','code':271,'data':None})
        user = User(loginname=loginname)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg':'OK','code':200,'data':{ 'username': user.loginname }})

