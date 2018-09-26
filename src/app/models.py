from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random
from datetime import datetime,timedelta

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
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

def props_with_(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value):
            pr[name] = value
    return pr


class School(db.Model):
    __tablename__ = 'Schools'

    id = db.Column("schoolid",db.Integer, primary_key=True)
    gradeid=db.Column("gradeid",db.Integer)
    gradename=db.Column("gradename",db.Integer)
    catid=db.Column("catid",db.Integer)
    catname = db.Column("catname",db.String(126))
    provid=db.Column("provid",db.Integer)
    provname = db.Column("provname",db.String(126))
    cityid=db.Column("cityid",db.Integer)
    cityname = db.Column("cityname",db.String(126))
    districtid=db.Column("districtid",db.Integer)
    districtname = db.Column("districtname",db.String(126))

    name = db.Column("schoolname",db.String(120), unique=True)
    desc = db.Column("schooldesc",db.String(1024))
    addr = db.Column("addr",db.String(126))
    tuition = db.Column("tuition",db.String(64))
    features = db.Column("features",db.String(1024))
    phone = db.Column("phone",db.String(32))
    intro = db.Column("intro",db.String(1024))
    team = db.Column("team",db.String(1024))
    founded = db.Column("founded",db.String(16))
    cityid = db.Column("cityid",db.String(64))
    age = db.Column("age",db.String(64))
    scale = db.Column("scale",db.String(64))
    population = db.Column("population",db.String(32))
    duration = db.Column("duration",db.String(32))
    foreignduration = db.Column("foreignduration",db.String(1024))
    schoolbus = db.Column("schoolbus",db.String(16))
    cramclass = db.Column("cramclass",db.String(16))
    sortindex =db.Column("sortindex",db.Integer)
    img = db.Column("img",db.String(126))
    thumb = db.Column("thumb",db.String(126))
    isbest = db.Column("isbest",db.Integer)
    isnew = db.Column("isnew",db.Integer)
    ishot = db.Column("ishot",db.Integer)
    istopshow = db.Column("istopshow",db.Integer)

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


    def to_dict(self):
        data = {
            'id': self.id,
            'catid':self.catid,
            'catname':self.catname,
            'gradeid':self.gradeid,
            'gradename':self.gradename,
            'name': self.name,
            'desc':self.desc,
            'addr': self.addr,
            'tuition': self.tuition,
            'features':self.features,
            'phone': self.phone,
            'intro': self.intro,
            'team':self.team,
            'provid':self.provid,
            'provname':self.provname,
            'cityid':self.cityid,
            'cityname':self.catname,
            'districtid':self.districtid,
            "districtname":self.districtname,
            'founded': self.founded,
            'age': self.age,
            'scale':self.scale,
            'population': self.population,
            'duration': self.duration,
            'foreignduration':self.foreignduration,
            'schoolbus': self.schoolbus,
            'cramclass': self.cramclass,
            'sortindex' :self.sortindex,
            'img': self.img,
            'thumb': self.thumb,
            'thumb_url':str(self.thumb)+'__',
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            }
        return data

class Province(db.Model):
    __tablename__ = 'Provinces'

    id = db.Column("provid",db.Integer, primary_key=True)
    name = db.Column("provname",db.String(120), unique=True)
    sortindex = db.Column("sortindex",db.Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data

class City(db.Model):
    __tablename__ = 'Cities'

    id = db.Column("cityid",db.Integer, primary_key=True)
    provid = db.Column("provid",db.Integer)
    name = db.Column("cityname",db.String(120))
    sortindex = db.Column("sortindex",db.Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name,'provid':self.provid}
        return data

class District(db.Model):
    __tablename__ = 'Districts'

    id = db.Column("districtid",db.Integer, primary_key=True)
    cityid = db.Column("cityid",db.Integer)
    name = db.Column("districtname",db.String(120), unique=True)
    sortindex = db.Column("sortindex",db.Integer)
    def to_dict(self):
        schoollist=None #[item.to_dict() for item in School.query.filter_by(districtid=self.id).all()]
        hotlist=None #[item.to_dict() for item in School.query.filter_by(districtid=self.id).filter_by(ishot=1).all()]
        data = {'id': self.id,'name': self.name,'text':self.name,'cityid':self.cityid,'schoollist':schoollist,'hotlist':hotlist}
        return data

class Grade(db.Model):
    __tablename__ = 'Grades'

    id = db.Column("gradeid",db.Integer, primary_key=True)
    name = db.Column("gradename",db.String(120), unique=True)
    desc = db.Column("gradedesc",db.String(120))
    sortindex = db.Column("sortindex",db.Integer)
    def to_dict(self):
        schools=[item.to_dict() for item in School.query.filter_by(gradeid=self.id).limit(6)]
        data = {'id': self.id,'name': self.name,'text':self.name,'schools':schools}
        return data
    def to_mini_dict(self):
        
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data

class Category(db.Model):
    __tablename__ = 'Categories'

    id = db.Column("catid",db.Integer, primary_key=True)
    name = db.Column("catname",db.String(120), unique=True)
    desc = db.Column("catdesc",db.String(120))
    sortindex = db.Column("sortindex",db.Integer)
    def to_dict(self):
        schools=[item.to_dict() for item in School.query.filter_by(catid=self.id)]
        data = {'id': self.id,'name': self.name,'text':self.name,'schools':schools}
        return data

    def to_mini_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data
        
class SmsCode(db.Model):
    __tablename__ = 'SmsCode'

    id = db.Column("smscodeid",db.Integer, primary_key=True)
    mobile = db.Column("mobile",db.String(120), unique=True)
    senddatetime = db.Column("senddatetime",db.String(120))
    verifycode = db.Column("verifycode",db.Integer)
    hasverified = db.Column("hasverified",db.String(120))
    createdbydatetime = db.Column("createdbydatetime",db.Integer)
    def to_dict(self):
        data = {'id': self.id,'mobile': self.mobile,'senddatetime':self.senddatetime,'verifycode':self.verifycode,'hasverified':self.hasverified}
        return data

    @staticmethod
    def send(mobileNo):
        sms = SmsCode.query.filter_by(mobile=mobileNo).order_by(SmsCode.id.desc()).first()
        if sms!=None:
            delta=datetime.now()-datetime.strptime(sms.senddatetime, '%Y-%m-%d %H:%M:%S')
            print(delta.total_seconds())
            if delta.total_seconds()<60:
                return ""
        code = ''
        for num in range(1,5):
            code = code + str(random.randint(0, 9))
        now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sms = SmsCode(mobile=mobileNo,verifycode=code,createdbydatetime=now)
        print(code)

        sms.senddatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        db.session.add(sms)
        db.session.commit()

        return "OK"
    
    @staticmethod    
    def verifyCode(mobileNo,code):
        sms = SmsCode.query.filter_by(mobile=mobileNo).order_by(desc(SmsCode.c.senddatetime)).first()
        if sms!=None and sms.verifycode==code:
            sms.update({'hasverified':True})
            db.session.commit()
            return True
        return False