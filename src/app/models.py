from app import app,db
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random
from datetime import datetime,timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired,BadSignature

goods_cats = [
    {
       'id': 1,
       'name': u'舞台剧',
       'text': u'舞台剧'
    },
    {
        'id': 2,
        'name': u'音乐剧',
        'text': u'音乐剧'  
    },
    {
        'id': 3,
        'name': u'音乐会',
        'text': u'音乐会'  
    },
    {
        'id': 4,
        'name': u'话剧',
        'text': u'话剧'  
    },
    {
        'id': 5,
        'name': u'展览',
        'text': u'展览'  
    },
    {
        'id': 6,
        'name': u'芭蕾舞剧',
        'text': u'芭蕾舞剧'  
    }
]

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

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        print(token)
        print(s)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user       

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

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
    lon = db.Column("lon",db.String(64))
    lat = db.Column("lat",db.String(64))
    cbdname = db.Column("cbdname",db.String(126))
    cbdid = db.Column("cbdid",db.Integer)
    shcoolpid = db.Column("shcoolpid",db.Integer)
    isbilingual = db.Column("isbilingual",db.Integer)
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
        galleryList=db.session.query(SchoolGallery).filter(SchoolGallery.objid==self.id)
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
            'cityname':self.cityname,
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
            'img_url':'/img/school/l/'+str(self.id),
            'thumb': self.thumb,
            'thumb_url':'/thumb/school/s/'+str(self.id),
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            'lon':self.lon,
            "lat":self.lat,
            "cbdname":self.cbdname,
            "cbdid":self.cbdid,
            "shcoolpid":self.shcoolpid,
            "isbilingual":self.isbilingual,
            'imglist':[{"id":g.id,"img":"/img/school/n/"+str(g.id)} for g in galleryList],
            }
        return data

class SchoolGallery(db.Model):
    __tablename__ = 'schoolgalleries'
    id =  db.Column("galleryid", db.Integer, primary_key=True)
    objid= db.Column("schoolid", db.Integer)
    title =  db.Column("imagetitle", db.String(120))
    desc =  db.Column("imagedesc", db.String(120))
    path =  db.Column("imagepath", db.String(120))
    isdefault =  db.Column("isdefault", db.Integer)
    istopshow =  db.Column("istopshow",db.Integer)
    isenable =  db.Column("isenable", db.Integer)
    cat =  db.Column("category", db.String(1))
    sortindex =  db.Column("sortindex", db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)


class Show(db.Model):

    __tablename__ = 'Shows'

    id = db.Column("showid",db.Integer, primary_key=True)
    catid = db.Column("catid",db.Integer)
    catname =db.Column("catname",db.String(128))
    name = db.Column("showname",db.String(120), unique=True)
    desc = db.Column("showdesc",db.String(1024))
    addr = db.Column("addr",db.String(128))
    features = db.Column("features",db.String(1024))
    phone = db.Column("phone",db.String(32))
    intro = db.Column("intro",db.String(1024))
    begindate = db.Column("begindate",db.String(64))
    enddate = db.Column("enddate",db.String(64))
    price = db.Column("price",db.Numeric(10,2))
    maxprice = db.Column("maxprice",db.Numeric(10,2))
    provid = db.Column("provid",db.Integer)
    provname = db.Column("provname",db.String(128))
    cityid = db.Column("cityid",db.Integer)
    cityname = db.Column("cityname",db.String(128))
    districtid = db.Column("districtid",db.Integer)
    districtname = db.Column("districtname",db.String(128))
    duration = db.Column("duration",db.String(32))
    sortindex = db.Column("sortindex",db.Integer)
    img = db.Column("img",db.String(126))
    thumb = db.Column("thumb",db.String(126))
    isbest = db.Column("isbest",db.Integer)
    isnew = db.Column("isnew",db.Integer)
    ishot = db.Column("ishot",db.Integer)
    istopshow = db.Column("istopshow",db.Integer)

    lon = db.Column("lon",db.String(64))
    lat = db.Column("lat",db.String(64))
    cbdname = db.Column("cbdname",db.String(126))
    cbdid = db.Column("cbdid",db.Integer)
 
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
        galleryList=db.session.query(ShowGallery).filter(ShowGallery.objid==self.id)
        data = {
            'id': self.id,
            'catid':self.catid,
            'catname':self.catname,
            'begindate':self.begindate,
            'enddate':self.enddate,
            'name': self.name,
            'desc':self.desc,
            'addr': self.addr,
            'features':self.features,
            'phone': self.phone,
            'intro': self.intro,
            'price':str(self.price),
            'maxprice':str(self.maxprice),
            'provid':self.provid,
            'provname':self.provname,
            'cityid':self.cityid,
            'cityname':self.cityname,
            'districtid':self.districtid,
            'districtname':self.districtname,
            'duration': self.duration,
            'sortindex':self.sortindex,
            'img': '/img/show/l/'+str(self.id),
            'thumb': '/img/show/s/'+str(self.id),
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            'lon':self.lon,#经度
            "lat":self.lat,#维度
            "cbdname":self.cbdname, #商圈名称
            "cbdid":self.cbdid,#商圈标识
            'imglist':[{"id":g.id,"img":"/img/show/n/"+str(g.id)} for g in galleryList],
            }
                
        return data

class ShowGallery(db.Model):
    __tablename__ = 'showgalleries'
    id =  db.Column("galleryid", db.Integer, primary_key=True)
    objid= db.Column("showid", db.Integer)
    title =  db.Column("imagetitle", db.String(120))
    desc =  db.Column("imagedesc", db.String(120))
    path =  db.Column("imagepath", db.String(120))
    isdefault =  db.Column("isdefault", db.Integer)
    istopshow =  db.Column("istopshow",db.Integer)
    isenable =  db.Column("isenable", db.Integer)
    cat =  db.Column("category", db.String(1))
    sortindex =  db.Column("sortindex", db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)


class Training(db.Model):

    __tablename__ = 'Trainings'

    id = db.Column("trainingid",db.Integer, primary_key=True)
    catid = db.Column("catid",db.Integer)
    catname =db.Column("catname",db.String(128))
    name = db.Column("trainingname",db.String(120), unique=True)
    desc = db.Column("trainingdesc",db.String(1024))
    team = db.Column("team",db.String(1024))
    content = db.Column("trainingcontent",db.String(1024))
    addr = db.Column("addr",db.String(128))
    features = db.Column("features",db.String(1024))
    phone = db.Column("phone",db.String(32))
    intro = db.Column("intro",db.String(1024))
    begindate = db.Column("begindate",db.String(64))
    enddate = db.Column("enddate",db.String(64))
    price = db.Column("price",db.Numeric(10,2))
    originalprice = db.Column("originalprice",db.Numeric(10,2))
    provid = db.Column("provid",db.Integer)
    provname = db.Column("provname",db.String(128))
    cityid = db.Column("cityid",db.Integer)
    cityname = db.Column("cityname",db.String(128))
    districtid = db.Column("districtid",db.Integer)
    districtname = db.Column("districtname",db.String(128))
    duration = db.Column("duration",db.String(32))
    sortindex = db.Column("sortindex",db.Integer)
    img = db.Column("img",db.String(126))
    thumb = db.Column("thumb",db.String(126))
    isbest = db.Column("isbest",db.Integer)
    isnew = db.Column("isnew",db.Integer)
    ishot = db.Column("ishot",db.Integer)
    istopshow = db.Column("istopshow",db.Integer)
    lon = db.Column("lon",db.String(64))
    lat = db.Column("lat",db.String(64))
    cbdname = db.Column("cbdname",db.String(126))
    cbdid = db.Column("cbdid",db.Integer)
 
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
        #classList=[ g.to_dict() for g in  db.session.query(TrainingClass).filter(TrainingClass.trainingid==self.id).limit(5)] 
        galleryList=db.session.query(TrainingGallery).filter(TrainingGallery.objid==self.id)
        data = {
            'id': self.id,
            'catid':self.catid,
            'catname':self.catname,
            'name': self.name,
            #'content':self.content,
            'desc':self.desc,
            'addr': self.addr,
            'team':self.team,
            'features':self.features,
            'phone': self.phone,
            'intro': self.intro,
            'price':str(self.price),
            'provid':self.provid,
            'provname':self.provname,
            'cityid':self.cityid,
            'cityname':self.cityname,
            'districtid':self.districtid,
            'districtname':self.districtname,
            'sortindex':self.sortindex,
            'img': '/img/training/l/'+str(self.id),
            'thumb': '/img/training/s/'+str(self.id),
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            'lon':self.lon,#经度
            'lat':self.lat,#维度
            'cbdname':self.cbdname, #商圈名称
            'cbdid':self.cbdid,#商圈标识

            'imglistforenv':[{"id":g.id,"img":"/img/training/n/"+str(g.id)} for g in galleryList if g.cat=='2' ],
            'imglist':[{"id":g.id,"img":"/img/training/n/"+str(g.id)} for g in galleryList if g.cat=='1' ],
            }
                
        return data
class TrainingClass(db.Model):

    __tablename__ = 'TrainingClasses'

    id = db.Column("classid",db.Integer, primary_key=True)
    trainingid = db.Column("trainingid",db.Integer)
    name = db.Column("classname",db.String(120), unique=True)
    desc = db.Column("classdesc",db.String(1024))
    content = db.Column("classcontent",db.String(1024))
    features = db.Column("features",db.String(1024))
    
    intro = db.Column("intro",db.String(1024))
    begindate = db.Column("begindate",db.String(64))
    enddate = db.Column("enddate",db.String(64))
    price = db.Column("price",db.Numeric(10,2))
    originalprice = db.Column("originalprice",db.Numeric(10,2))
    
    duration = db.Column("duration",db.String(32))
    sortindex = db.Column("sortindex",db.Integer)
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
        return str(self.name)
    
    def to_dict(self):
       
        data = {
            'id': self.id,
           
            'begindate':self.begindate,
            'enddate':self.enddate,
            'name': self.name,
            'content':self.content,
            'desc':self.desc,
            
            'features':self.features,
            
            'intro': self.intro,
            'price':str(self.price),
            'originalprice':str(self.originalprice),
            
            'duration': self.duration,
            'sortindex':self.sortindex,
            'img': '/img/class/l/'+str(self.id),
            'thumb': '/img/class/s/'+str(self.id),
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,

            }
                
        return data

class TrainingGallery(db.Model):
    __tablename__ = 'traininggalleries'
    id =  db.Column("galleryid", db.Integer, primary_key=True)
    objid= db.Column("trainingid", db.Integer)
    title =  db.Column("imagetitle", db.String(120))
    desc =  db.Column("imagedesc", db.String(120))
    path =  db.Column("imagepath", db.String(120))
    isdefault =  db.Column("isdefault", db.Integer)
    istopshow =  db.Column("istopshow",db.Integer)
    isenable =  db.Column("isenable", db.Integer)
    cat =  db.Column("category", db.String(1))
    sortindex =  db.Column("sortindex", db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)




class Lecturer(db.Model):

    __tablename__ = 'Lecturers'

    id = db.Column("lecturerid",db.Integer, primary_key=True)
    catid = db.Column("catid",db.Integer)
    catname =db.Column("catname",db.String(128))
    name = db.Column("lecturername",db.String(120), unique=True)
    desc = db.Column("lecturerdesc",db.String(1024))
    team = db.Column("team",db.String(1024))
    content = db.Column("lecturercontent",db.String(1024))
    addr = db.Column("addr",db.String(128))
    features = db.Column("features",db.String(1024))
    phone = db.Column("phone",db.String(32))
    intro = db.Column("intro",db.String(1024))
    begindate = db.Column("begindate",db.String(64))
    enddate = db.Column("enddate",db.String(64))
    price = db.Column("price",db.Numeric(10,2))
    provid = db.Column("provid",db.Integer)
    provname = db.Column("provname",db.String(128))
    cityid = db.Column("cityid",db.Integer)
    cityname = db.Column("cityname",db.String(128))
    districtid = db.Column("districtid",db.Integer)
    districtname = db.Column("districtname",db.String(128))
    duration = db.Column("duration",db.String(32))
    sortindex = db.Column("sortindex",db.Integer)
    img = db.Column("img",db.String(126))
    thumb = db.Column("thumb",db.String(126))
    isbest = db.Column("isbest",db.Integer)
    isnew = db.Column("isnew",db.Integer)
    ishot = db.Column("ishot",db.Integer)
    istopshow = db.Column("istopshow",db.Integer)
    lon = db.Column("lon",db.String(64))
    lat = db.Column("lat",db.String(64))
    cbdname = db.Column("cbdname",db.String(126))
    cbdid = db.Column("cbdid",db.Integer)
 
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
            'catid':self.catid,
            'catname':self.catname,
            'name': self.name,
            'content':self.content,
            'desc':self.desc,
            'features':self.features,
            'intro': self.intro,
            'sortindex':self.sortindex,
            'img': self.img,
            'thumb': self.thumb,
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            "title":self.title
            }
                
        return data

class LecturerGallery(db.Model):
    __tablename__ = 'lecturergalleries'
    id = db.Column("galleryid",db.Integer, primary_key=True)
    objid=db.Column("trainingid",db.Integer)
    title = db.Column("imagetitle",db.String(120))
    desc = db.Column("imagedesc",db.String(120))
    path = db.Column("imagepath",db.String(120))
    isdefault = db.Column("isdefault",db.Integer)
    istopshow = db.Column("istopshow",db.Integer)
    isenable = db.Column("isenable",db.Integer)
    cat = db.Column("category",db.String(1))
    sortindex = db.Column("sortindex",db.Integer)

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
        data = {
            'id': self.id,
            'objid':self.objid,
            'title': self.title,
            'text':self.title,
            'path':self.path,
            'cat':self.cat,
            'isdefault': self.isdefault,
            'istopshow':self.istopshow,
            'isenable':self.isenable,
            'sortindex':self.sortindex,
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

class CBD(db.Model):
    __tablename__ = 'Cbds'

    id = db.Column("cbdid",db.Integer, primary_key=True)
    districtid = db.Column("districtid",db.Integer)
    name = db.Column("cbdname",db.String(120), unique=True)
    sortindex = db.Column("sortindex",db.Integer)
    def to_dict(self):
        schoollist=None #[item.to_dict() for item in School.query.filter_by(districtid=self.id).all()]
        hotlist=None #[item.to_dict() for item in School.query.filter_by(districtid=self.id).filter_by(ishot=1).all()]
        data = {'id': self.id,'name': self.name,'text':self.name,'districtid':self.districtid,'schoollist':schoollist,'hotlist':hotlist}
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
    typeid = db.Column("typeid",db.Integer)
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
            if delta.total_seconds()<60:
                return 60-delta.total_seconds()
        code = ''
        for num in range(1,5):
            code = code + str(random.randint(0, 9))
        code='0000'
        now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sms = SmsCode(mobile=mobileNo,verifycode=code,createdbydatetime=now)
        
        sms.senddatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        db.session.add(sms)
        db.session.commit()

        return 60
    
    @staticmethod    
    def verifyCode(mobileNo,code):
        sms = SmsCode.query.filter_by(mobile=mobileNo).order_by(desc(SmsCode.c.senddatetime)).first()
        if sms!=None and sms.verifycode==code and 60>(datetime.now()-datetime.strptime(sms.senddatetime, '%Y-%m-%d %H:%M:%S')) :
            sms.update({'hasverified':True})
            db.session.commit()
            return True
        return False