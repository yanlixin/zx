from flask_login import LoginManager,UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Column, Integer,SmallInteger, String, ForeignKey, DateTime,Boolean,and_,or_
#from sqlalchemy.dialects.postgresql as  import UUID as pg
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime  
from app import db
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

class Project(db.Model,BaseModel):
    __tablename__ = 'PM_Projects'
    id = Column("ProjectID",pg.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    no = Column("ProjectNo",String(64), unique=True)
    name = Column("ProjectName",String(512), unique=True)
    fullname = Column("ProjectFullName",String(512), unique=True)
    desc = Column("ProjectDesc",String(1024))
    remark = Column("Remark",String(1024))
    memo = Column("Memo",String(16))
    extradata = Column("ExtraData",pg.JSONB)
    status = Column("RecordStatus",SmallInteger)
    createdbydate = Column("CreatedDate",DateTime)
    createdbymanagerid = Column("CreatedByUserID",Integer)
    lastupdatedbydate = Column("LastedDate",DateTime)
    lastupdatedbymanagerid = Column("LastedByUserID",Integer)
   
    def to_dict(self):
        
        data = {'id': str(self.id),'no':self.no,'name': self.name,'fullname':self.fullname,'desc':self.desc}
        return data

    @staticmethod
    def select():
        return db.session.query(Project).filter(Project.status==0)


    