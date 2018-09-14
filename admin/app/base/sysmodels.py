from flask_login import LoginManager,current_user
from app import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
from datetime import datetime  

class Permission:
    FOLLOW = 0x01 #关注其他用户
    COMMENT = 0x02 #评论
    WHITE_ARTICLES = 0x04 #写文章
    MODERATE_COMMENTS = 0x08 #管理评论
    ADMINISTER = 0x80 #管理员权限

class BaseModel():
    id=0
    status =0
    createdbydate = datetime.now()
    createdbymanagerid = 0
    lastupdatedbydate = datetime.now()
    lastupdatedbymanagerid = 0
    csrf_token=""

    @property
    def status_text( self ):
        print('a')
        print(self.status)
        dict = {"0" : "正常", "1" : "已删除", "2" : "已禁用", "3" : "已提交"}
        return dict.get(self.status)

    def mark_del(self,mangerId):
        self.status=1
        self.lastupdatedbydate=datetime.now()
        self.lastupdatedbymanagerid=mangerId
        data = {'id': self.id,'status': self.status,'lastupdatedbydate':self.lastupdatedbydate,'lastupdatedbymanagerid':self.lastupdatedbymanagerid}
        return data

    def mark_update(self,mangerId):
        self.lastupdatedbydate=datetime.now()
        self.lastupdatedbymanagerid=mangerId

    def mark_add(self,mangerId):
        self.status=0
        self.createdbydate=datetime.now()
        self.createdbymanagerid=mangerId
        self.lastupdatedbydate=datetime.now()
        self.lastupdatedbymanagerid=mangerId

class Role(db.Model,BaseModel):
    __tablename__ = 'Roles'
    id = Column("roleid",Integer, primary_key=True)
    name = Column("rolename",String(120), unique=True)
    desc = Column("roledesc",String(120))
    issys = Column("IsSys",String(120))
    sortindex = Column("sortindex",Integer)
    status = Column("recordstatus",Integer)
    createdbydate = Column("createdbydate",String(32))
    createdbymanagerid = Column("createdbymanagerid",Integer)
    lastupdatedbydate = Column("lastupdatedbydate",String(32))
    lastupdatedbymanagerid = Column("lastupdatedbymanagerid",Integer)
   
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'desc':self.desc}
        return data

 
class UserRole(db.Model):
    __tablename__ = 'R_Users_Roles'
    id = Column("ruserroleid",Integer, primary_key=True)
    managerid = Column("managerid",String(120), unique=True)
    roleid = Column("roleid",String(120))
    recordstatus = Column("recordstatus",Integer)
    createdbydate = Column("createdbydate",String(32))
    createdbymanagerid = Column("createdbymanagerid",Integer)
    lastupdatedbydate = Column("lastupdatedbydate",String(32))
    lastupdatedbymanagerid = Column("lastupdatedbymanagerid",Integer)
    def to_dict(self):
        data = {'id': self.id}
        return data

class Permissions(db.Model):
    __tablename__ = 'Permissions'
    id = Column("permid",Integer, primary_key=True)
    permuuid = Column("permuuid",String(120), unique=True)
    name = Column("permname",String(120), unique=True)
    desc = Column("roledesc",String(120))
    issys = Column("IsSys",String(120))
    sortindex = Column("sortindex",Integer)
    recordstatus = Column("recordstatus",Integer)
    createdbydate = Column("createdbydate",String(32))
    createdbymanagerid = Column("createdbymanagerid",Integer)
    lastupdatedbydate = Column("lastupdatedbydate",String(32))
    lastupdatedbymanagerid = Column("lastupdatedbymanagerid",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name,'desc':self.desc}
        return data

class PermissionRole(db.Model):
    __tablename__ = 'R_Permissions_Roles'
    id = Column("rpermroleid",Integer, primary_key=True)
    roleid = Column("roleid",String(120), unique=True)
    permid = Column("permid",String(120))
    createdbydate = Column("createdbydate",String(32))
    createdbymanagerid = Column("createdbymanagerid",Integer)
    def to_dict(self):
        data = {'id': self.id}
        return data