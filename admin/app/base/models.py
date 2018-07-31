from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
from datetime import datetime  


class User(db.Model, UserMixin):
    __tablename__ = 'managers'

    id = Column("managerid",Integer, primary_key=True)
    username = Column("loginname",String(64), unique=True)
    email = Column("email",String(64), unique=True)
    password = Column("loginpwd",String(30))
    createdbydate = Column("createdbydate",DateTime(), default=datetime.now)
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


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

class Category(db.Model):
    __tablename__ = 'Categories'

    id = Column("catid",Integer, primary_key=True)
    name = Column("catname",String(120), unique=True)
    desc = Column("catdesc",String(120))
    sortindex = Column("sortindex",Integer)


class School(db.Model):

    __tablename__ = 'Schools'

    id = Column("schoolid",Integer, primary_key=True)
    name = Column("schoolname",String(120), unique=True)
    desc = Column("schooldesc",String(1024))
    addr = Column("addr",String(126))
    tuition = Column("tuition",String(64))
    features = Column("features",String(1024))
    phone = Column("phone",String(32))
    intro = Column("intro",String(1024))
    team = Column("team",String(1024))
    founded = Column("founded",String(16))
    districtid = Column("districtid",Integer)
    age = Column("age",String(64))
    scale = Column("scale",String(64))
    population = Column("population",String(32))
    duration = Column("duration",String(32))
    foreignduration = Column("foreignduration",String(1024))
    schoolbus = Column("schoolbus",String(16))
    cramclass = Column("cramclass",String(16))
    sortindex = Column("sortindex",Integer)
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'desc':self.desc,
            'addr': self.addr,
            'tuition': self.tuition,
            'features':self.features,
            'phone': self.phone,
            'intro': self.intro,
            'team':self.team,
            'districtid':self.districtid,
            'founded': self.founded,
            'age': self.age,
            'scale':self.scale,
            'population': self.population,
            'duration': self.duration,
            'foreignduration':self.foreignduration,
            'schoolbus': self.schoolbus,
            'cramclass': self.cramclass,
            'sortindex':self.sortindex,
            }
        return data