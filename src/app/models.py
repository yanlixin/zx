from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    loginname = db.Column(db.String(64), index = True, unique = True)
    loginpwd = db.Column(db.String(64), index = True, unique = True)
    nickname = db.Column(db.String(64), index = True, unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(20), index = True, unique = False)
    createdbydate = db.Column(db.String(20), index = True, unique = False)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return True

    def check_password(self, password):
        return True #check_password_hash(self.password_hash, password)
    def set_password(self, password):
            self.password_hash = generate_password_hash(password)
    

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    def to_dict(self, include_email=False):
        data = {
            'id': self.id
          
        }
       
        return data

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'rows': [item.to_dict() for item in resources.items],
            'total' : 100
           
        }
        return data

    def __repr__(self):
        return '<User %r>' % (self.nickname)
    
class School(db.Model):

    __tablename__ = 'School'

    id = db.Column(db.Integer, primary_key=True)
    schoolname = db.Column(db.String(120), unique=True)
    schooldesc = db.Column(db.String(1024))
    addr = db.Column(db.String(126))
    tuition = db.Column(db.String(64))
    features = db.Column(db.String(1024))
    phone = db.Column(db.String(32))
    intro = db.Column(db.String(1024))
    team = db.Column(db.String(1024))
    founded = db.Column(db.String(16))
    city = db.Column(db.String(64))
    age = db.Column(db.String(64))
    size = db.Column(db.String(64))
    population = db.Column(db.String(32))
    duration = db.Column(db.String(32))
    foreignduration = db.Column(db.String(1024))
    schoolbus = db.Column(db.String(16))
    cramclass = db.Column(db.String(16))
    
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