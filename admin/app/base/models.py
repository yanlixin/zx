from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime  ,and_,or_
from datetime import datetime  

from .basemodels import BaseModel
from .sysmodels import User,Role,UserRole,PermissionRole,Permission

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

