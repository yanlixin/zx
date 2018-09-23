from flask_login import LoginManager,UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Column, Integer,SmallInteger, String, ForeignKey, DateTime,Boolean,and_,or_
#from sqlalchemy.dialects.postgresql as  import UUID as pg
import sqlalchemy.dialects.postgresql as pg
import psycopg2 as pg2
import psycopg2.extensions as pg2e
from datetime import datetime  
from app import db
from app.config  import Config
import uuid

from app.base.basemodels import BaseModel

from json import JSONEncoder
#from uuid import UUID

JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, uuid.UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault

def generate_uuid():
    return str(uuid.uuid4())

UUID_DEF='5edbfcbb-1df8-48fa-853f-7917e4e346db'

def loimport(data):
    lo=pg2.connect("").lobject()
    lo.write(data)
    return lo 
class Project(db.Model,BaseModel):
    __tablename__ = 'PM_Projects'
    id = Column("ProjectID",pg.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    no = Column("ProjectNo",String(64), unique=True)
    name = Column("ProjectName",String(512), unique=True)
    fullname = Column("ProjectFullName",String(512), unique=True)
    desc = Column("ProjectDesc",String(1024))
    remark = Column("Remark",String(1024))
    memo = Column("Memo",String(1024))
    extradata = Column("ExtraData",pg.JSONB)
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
    def to_dict(self):
        
        data = {'id': str(self.id),'no':self.no,'name': self.name,'fullname':self.fullname,'desc':self.desc}
        return data

    @staticmethod
    def select():
        return db.session.query(Project).filter(Project.status==0)


class Task(db.Model,BaseModel):
    __tablename__ = 'PM_Tasks'
    id = Column("TaskID",pg.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    projid=Column("ProjectID",pg.UUID(as_uuid=True))
    pid=Column("TaskPID",pg.UUID(as_uuid=True))
    name = Column("TaskName",String(512))
    no = Column("TaskNo",String(512))
    desc = Column("TaskDesc",String(1024))
    memo = Column("Memo",String(1024))
    extradata = Column("ExtraData",pg.JSONB)
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
   
    def to_dict(self):
        
        data = {'id': str(self.id),'name': self.name,'desc':self.desc}
        return data

    @staticmethod
    def select():
        return db.session.query(Deliverable).filter(Deliverable.status==0)

class Deliverable(db.Model,BaseModel):
    __tablename__ = 'PM_Deliverables'
    id = Column("DeliverableID",pg.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    projid=Column("ProjectID",pg.UUID(as_uuid=True))
    name = Column("DeliverableName",String(512))
    no = Column("DeliverableNo",String(64))
    desc = Column("DeliverableDesc",String(1024))
    remark = Column("Remark",String(1024))
    memo = Column("Memo",String(1024))
    extradata = Column("ExtraData",pg.JSONB)
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
   
    def to_dict(self):
        
        data = {'id': str(self.id),'name': self.name,'desc':self.desc}
        return data

    @staticmethod
    def select():
        return db.session.query(Deliverable).filter(Deliverable.status==0)

class TeamMember(db.Model,BaseModel):
    __tablename__ = 'PM_TeamMembers'
    id = Column("TeamMemberID",pg.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    projid=Column("ProjectID",pg.UUID(as_uuid=True))
    user=Column("UserID",Integer)
    loginname = Column("LoginName",String(64))
    ismanager = Column("IsManager",db.Boolean)
    desc = Column("DeliverableDesc",String(1024))
    extradata = Column("ExtraData",pg.JSONB)
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
   
    def to_dict(self):
        
        data = {'id': str(self.id),'name': self.name,'desc':self.desc}
        return data

    @staticmethod
    def select():
        return db.session.query(TeamMember).filter(TeamMember.status==0)   

class DocCat(db.Model,BaseModel):
    __tablename__ = 'PM_DocCategories'
    id = Column("DocCatID",pg.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    projid=Column("ProjectID",pg.UUID(as_uuid=True))
    no = Column("CatNo",String(64))
    name = Column("CatName",String(64))
    desc = Column("CatDesc",String(1024))
    isrequired = Column("IsRequired",pg.BOOLEAN)
    
    preview = Column("Preview",pg.OID)
    extradata = Column("ExtraData",pg.JSONB)
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
   
    def to_dict(self):
        
        data = {'id': str(self.id),'name': self.name,'desc':self.desc,'isrequired':self.isrequired}
        return data

    @staticmethod
    def select():
        return db.session.query(DocCats).filter(DocCats.status==0)   
    
class Doc(db.Model,BaseModel):
    __tablename__ = 'PM_Docs'
    id = Column("DocID",pg.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    projid=Column("ProjectID",pg.UUID(as_uuid=True))
    catid=Column("DocCatID",pg.UUID(as_uuid=True))
    no = Column("DocNo",String(64))
    title = Column("Title",String(64))
    fullname = Column("FullName",String(64))
    alias = Column("Alias",String(64))
    filetype = Column("FileType",String(64))
    desc = Column("Desc",String(1024))
    memo = Column("Memo",String(1024))
    summary = Column("Summary",String(1024))
    lastedversion = Column("LastedVersion",String(1024))
    preview = Column("Preview",pg.BYTEA)
    filedata = Column("FileData",pg.BYTEA)
    extradata = Column("ExtraData",pg.JSONB)
    status = Column("RecordStatus",SmallInteger)
    createddate = Column("CreatedDate",DateTime)
    createdbyuserid = Column("CreatedByUserID",Integer)
    lasteddate = Column("LastedDate",DateTime)
    lastedbyuserid = Column("LastedByUserID",Integer)
   
    def to_dict(self):
        
        data = {'id': str(self.id),'no':self.no,'title': self.title,'desc':self.desc,'catid':self.catid,'fullname':self.fullname,'alias':self.alias}
        return data

    @staticmethod
    def select():
        return db.session.query(Doc).filter(Doc.status==0)   