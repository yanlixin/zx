from flask_login import LoginManager,current_user
from app import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
from datetime import datetime  
from .basemodels import BaseModel
class Permission:
    FOLLOW = 0x01 #关注其他用户
    COMMENT = 0x02 #评论
    WHITE_ARTICLES = 0x04 #写文章
    MODERATE_COMMENTS = 0x08 #管理评论
    ADMINISTER = 0x80 #管理员权限

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
    @staticmethod
    def select():
        return db.session.query(Role).filter(Role.status==0)
 
class UserRole(db.Model,BaseModel):
    __tablename__ = 'R_Users_Roles'
    id = Column("ruserroleid",Integer, primary_key=True)
    managerid = Column("managerid",String(120), unique=True)
    roleid = Column("roleid",String(120))
    status = Column("recordstatus",Integer)
    createdbydate = Column("createdbydate",String(32))
    createdbymanagerid = Column("createdbymanagerid",Integer)
    lastupdatedbydate = Column("lastupdatedbydate",String(32))
    lastupdatedbymanagerid = Column("lastupdatedbymanagerid",Integer)
    def to_dict(self):
        data = {'id': self.id}
        return data
    @staticmethod
    def write_data(managerid,roleids):
        db.session.query(UserRole).filter(UserRole.managerid==managerid)\
        .filter(UserRole.status==0).filter(~UserRole.roleid.in_([roleids]))\
        .update(UserRole().mark_del(),synchronize_session='fetch')
        db.session.commit()

        rolelist=roleids.split(",")
        for roleid in rolelist:
            userRole=UserRole(managerid=managerid,roleid=roleid)
            userRole.mark_add()
            db.session.add(userRole)
        db.session.commit()

    @staticmethod
    def select():
        return db.session.query(UserRole).filter(UserRole.status==0)

class Permission(db.Model):
    __tablename__ = 'Permissions'
    id = Column("permid",Integer, primary_key=True)
    uuid = Column("permuuid",String(120), unique=True)
    name = Column("permname",String(120), unique=True)
    desc = Column("permdesc",String(120))
    group = Column("permgroup",String(120))
    issys = Column("IsSys",String(120))
    createdbydate = Column("createdbydate",String(32))
    createdbymanagerid = Column("createdbymanagerid",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'desc':self.desc,'group':self.group}
        return data

    @staticmethod
    def select():
        return db.session.query(Permission)

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

    @staticmethod
    def select():
        return db.session.query(PermissionRole)