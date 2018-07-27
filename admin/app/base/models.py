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

class District(db.Model):
    __tablename__ = 'Districts'

    id = Column("districtid",Integer, primary_key=True)
    name = Column("districtname",String(120), unique=True)
    sortindex = Column("sortindex",Integer)

class Category(db.Model):
    __tablename__ = 'Categoies'

    id = Column("catid",Integer, primary_key=True)
    name = Column("catname",String(120), unique=True)
    desc = Column("catdesc",String(120))
    sortindex = Column("sortindex",Integer)


class School(db.Model):

    __tablename__ = 'Schools'

    id = Column(Integer, primary_key=True)
    schoolname = Column(String(120), unique=True)
    schooldesc = Column(String(1024))
    addr = Column(String(126))
    tuition = Column(String(64))
    features = Column(String(1024))
    phone = Column(String(32))
    intro = Column(String(1024))
    team = Column(String(1024))
    founded = Column(String(16))
    city = Column(String(64))
    age = Column(String(64))
    size = Column(String(64))
    population = Column(String(32))
    duration = Column(String(32))
    foreignduration = Column(String(1024))
    schoolbus = Column(String(16))
    cramclass = Column(String(16))
    
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
        return str(self.schoolname)