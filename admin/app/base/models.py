from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
from datetime import datetime  
from werkzeug.security import generate_password_hash,check_password_hash
from .basemodels import BaseModel

class User(db.Model, UserMixin,BaseModel):
    __tablename__ = 'managers'

    id = Column("managerid",Integer, primary_key=True)
    displayname = Column("managername",String(64), unique=True)
    loginname = Column("loginname",String(64), unique=True)
    email = Column("email",String(64))
    mobile = Column("mobile",String(64))
    desc = Column("desc",String(512))
    remark = Column("remark",String(512))
    password = Column("loginpwd",String(30))
    ismaster=Column("ismaster",Integer)
    status = Column("recordstatus",Integer)
    createdbydate = Column("createdbydate",String(32))
    createdbymanagerid = Column("createdbymanagerid",Integer)
    lastupdatedbydate = Column("lastupdatedbydate",String(32))
    lastupdatedbymanagerid = Column("lastupdatedbymanagerid",Integer)
    @property
    def username(self):
        return self.loginname

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)

    def to_dict(self):
        data = {'id': self.id,'displayname': self.displayname,'loginname':self.loginname,'email':self.email,'mobile':self.mobile,'desc':self.desc,'remark':self.remark}
        return data

    def __repr__(self):
        return str(self.username)

    def can(self, permissions):
        #return self.role is not None and (self.role.permissions & permissions) == permissions
        if self.is_master:
            return True
        return False

    def is_master(self):
        return self.ismaster==1

    def gen_password(self,pwd):
        self.password = generate_password_hash(pwd)
        return self.password

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

class Province(db.Model):
    __tablename__ = 'Provinces'

    id = Column("provid",Integer, primary_key=True)
    name = Column("provname",String(120), unique=True)
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data

class City(db.Model):
    __tablename__ = 'Cities'

    id = Column("cityid",Integer, primary_key=True)
    provid = Column("provid",Integer)
    name = Column("cityname",String(120))
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name,'provid':self.provid}
        return data

class District(db.Model):
    __tablename__ = 'Districts'

    id = Column("districtid",Integer, primary_key=True)
    cityid = Column("cityid",Integer)
    name = Column("districtname",String(120), unique=True)
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name,'cityid':self.cityid}
        return data

class Grade(db.Model):
    __tablename__ = 'Grades'

    id = Column("gradeid",Integer, primary_key=True)
    name = Column("gradename",String(120), unique=True)
    desc = Column("gradedesc",String(120))
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data

class Category(db.Model):
    __tablename__ = 'Categories'

    id = Column("catid",Integer, primary_key=True)
    name = Column("catname",String(120), unique=True)
    desc = Column("catdesc",String(120))
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data

