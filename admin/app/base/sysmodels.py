from flask_login import LoginManager,UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Column, Integer,SmallInteger, String, ForeignKey, DateTime,Boolean,and_,or_
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime  
from app import db


from .basemodels import BaseModel




class User(db.Model, UserMixin,BaseModel):
    __tablename__ = 'Users'

    id = Column("UserID",Integer, primary_key=True)
    displayname = Column("UserName",String(64), unique=True)
    loginname = Column("LoginName",String(64), unique=True)
    email = Column("EMail",String(64))
    mobile = Column("Mobile",String(64))
    desc = Column("UserDesc",String(512))
    remark = Column("Remark",String(512))
    password = Column("LoginPwd",String(30))
    ismaster=Column("IsMaster",db.Boolean)
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
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
        print(permissions,self.is_master)
        #return self.role is not None and (self.role.permissions & permissions) == permissions
        if self.is_master:
            return True
        sql = db.session.query(UserRole.roleid).join(User).join(Role).filter(and_(Role.status==0,User.status==0,UserRole.status==0)) 
        num = db.session.query(PermissionRole).join(Permission).filter(and_(Permission.uuid==permissions,PermissionRole.roleid.in_(sql))) 
        print("num",num)
        return num.count() >0
    @property
    def is_master(self):
        return self.ismaster==1

    def gen_password(self,pwd):
        self.password = generate_password_hash(pwd)
        return self.password

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Role(db.Model,BaseModel):
    __tablename__ = 'Roles'
    id = Column("RoleID",Integer, primary_key=True)
    name = Column("RoleName",String(120), unique=True)
    desc = Column("RoleDesc",String(120))
    issys = Column("IsSys",Boolean)
    sortindex = Column("SortIndex",String(16))
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
   
    def to_dict(self):
        
        data = {'id': self.id,'name': self.name,'desc':self.desc}
        return data
    @staticmethod
    def select():
        return db.session.query(Role).filter(Role.status==0)
 
class UserRole(db.Model,BaseModel):
    __tablename__ = 'R_Users_Roles'
    id = Column("RUserRoleID",Integer, primary_key=True)
    managerid = Column("UserID",String(120), ForeignKey('Users.UserID'))
    roleid = Column("RoleID",Integer,ForeignKey('Roles.RoleID'))
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
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
    id = Column("PermID",Integer, primary_key=True)
    uuid = Column("PermKey",String(120), unique=True)
    name = Column("PermName",String(120), unique=True)
    desc = Column("PermDesc",String(120))
    group = Column("PermGroup",String(120))
    issys = Column("IsSys",Boolean)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'desc':self.desc,'group':self.group}
        return data

    @staticmethod
    def select():
        return db.session.query(Permission)

class PermissionRole(db.Model):
    __tablename__ = 'R_Permissions_Roles'
    id = Column("RPermRoleID",Integer, primary_key=True)
    permid = Column("PermID",Integer,ForeignKey('Permissions.PermID'))
    roleid = Column("RoleID",Integer, ForeignKey('Roles.RoleID'))
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    def to_dict(self):
        data = {'id': self.id,"permid":self.permid,"roleid":self.roleid}
        return data

    @staticmethod
    def write_data(roleid,permids):
        db.session.query(PermissionRole).filter(PermissionRole.roleid==roleid).delete(synchronize_session='fetch')
        db.session.commit()

        permlist=permids.split(",")
        for permid in permids:
            permissionRole=PermissionRole(roleid=roleid,permid=permid)
            db.session.add(permissionRole)
        db.session.commit()
    @staticmethod
    def select():
        return db.session.query(PermissionRole)


def fill_user_role():
    sql=db.session.query(UserRole.id,User.loginname,User.id,Role.id,Role.name).join(User).join(Role)\
    .filter(and_(Role.status==0,User.status==0,UserRole.status==0))    
    

def fill_role_perm():
    sql=db.session.query(PermissionRole.id,Permission.uuid,Permission.id,Role.id,Role.name).join(Permission).join(Role)\
    .filter(and_(Role.status==0))
