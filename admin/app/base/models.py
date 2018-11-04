from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Numeric
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


class CBD(db.Model):
    __tablename__ = 'CBDs'

    id = Column("cbdid",Integer, primary_key=True)
    distid = Column("districtid",Integer)
    name = Column("cbdname",String(120), unique=True)
    desc = Column("cbddesc",String(256), unique=True)
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name,'desc':self.desc,'distid':self.distid}
        return data
    def to_data(self):
        data = {'id': self.id,'name': self.name,'desc':self.desc,'distid':self.distid}
        return data
        

class Grade(db.Model):
    __tablename__ = 'Grades'

    id = Column("gradeid",Integer, primary_key=True)
    name = Column("gradename",String(120), unique=True)
    desc = Column("gradedesc",String(120))
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data

class Category(db.Model):
    __tablename__ = 'Categories'

    id = Column("catid",Integer, primary_key=True)
    typeid = Column("typeid",Integer,)
    typename = Column("typename",String(120), unique=True)
    name = Column("catname",String(120), unique=True)
    desc = Column("catdesc",String(120))
    sortindex = Column("sortindex",Integer)
    def to_dict(self):
        data = {'id': self.id,'name': self.name,'text':self.name}
        return data

    def to_data(self):
        data = {'id': self.id,'name': self.name,'desc':self.desc,"typeid":self.typeid,"typename":self.typename}
        return data
    @staticmethod
    def list(typeid):
        data=db.session.query(Category).filter(Category.typeid==typeid).all()
        return data    
class School(db.Model):

    __tablename__ = 'Schools'

    id = Column("schoolid",Integer, primary_key=True)
    catid = Column("catid",Integer)
    catname =Column("catname",String(128))
    gradeid = Column("gradeid",Integer)
    gradename =Column("gradename",String(128))
    name = Column("schoolname",String(120), unique=True)
    desc = Column("schooldesc",String(1024))
    addr = Column("addr",String(128))
    tuition = Column("tuition",String(64))
    features = Column("features",String(1024))
    phone = Column("phone",String(32))
    intro = Column("intro",String(1024))
    team = Column("team",String(1024))
    founded = Column("founded",String(16))
    provid = Column("provid",Integer)
    provname = Column("provname",String(128))
    cityid = Column("cityid",Integer)
    cityname = Column("cityname",String(128))
    districtid = Column("districtid",Integer)
    districtname = Column("districtname",String(128))
    age = Column("age",String(64))
    scale = Column("scale",String(64))
    population = Column("population",String(32))
    duration = Column("duration",String(32))
    foreignduration = Column("foreignduration",String(1024))
    schoolbus = Column("schoolbus",String(16))
    cramclass = Column("cramclass",String(16))
    sortindex = Column("sortindex",Integer)
    img = Column("img",String(126))
    thumb = Column("thumb",String(126))
    isbest = Column("isbest",Integer)
    isnew = Column("isnew",Integer)
    ishot = Column("ishot",Integer)
    istopshow = Column("istopshow",Integer)

    lon = Column("lon",String(64))
    lat = Column("lat",String(64))
    cbdname = Column("cbdname",String(126))
    cbdid = Column("cbdid",Integer)
    shcoolpid = Column("shcoolpid",Integer)
    isbilingual = Column("isbilingual",Integer)
    price = Column("price",Numeric(10,2))

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
            'districtname':self.districtname,
            'founded': self.founded,
            'age': self.age,
            'scale':self.scale,
            'population': self.population,
            'duration': self.duration,
            'foreignduration':self.foreignduration,
            'schoolbus': self.schoolbus,
            'cramclass': self.cramclass,
            'sortindex':self.sortindex,
            'img': self.img,
            'thumb': self.thumb,
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            'lon':self.lon,#经度
            "lat":self.lat,#维度
            "cbdname":self.cbdname, #商圈名称
            "cbdid":self.cbdid,#商圈标识
            "shcoolpid":self.shcoolpid, #预留
            "isbilingual":self.isbilingual, #是否 
            "price":self.price #是否 
            
            }
                
        return data
    @staticmethod
    def get_column_names():
        data = [
            'id',
            'catname',#分类
            'gradeid',
            'gradename',#等级
            'name',#名称
            'desc',#描述
            'addr',#地址
            'tuition',#学费
            'features',#特色简介
            'phone',#电话
            'intro',#介绍
            'team',#团队介绍
            'provname',#省
            'cityname',#城市
            'districtname',#区
            'founded',#建校时间
            'age',#学生年龄段
            'scale',#学校规模
            'population',#师生数
            'duration',#上课时间
            'foreignduration',#外教授课时长
            'schoolbus',#校车
            'cramclass',#课后托班
            'sortindex',#排序
            'lon',#经度
            "lat",#维度
            "cbdname", #商圈名称
            "cbdid",#商圈标识
            "shcoolpid", #预留
            "isbilingual" #是否双语 
            ]
                
        return data

class SchoolGallery(db.Model):
    __tablename__ = 'schoolgalleries'
    id = Column("galleryid",Integer, primary_key=True)
    objid=Column("schoolid",Integer)
    title = Column("imagetitle",String(120))
    desc = Column("imagedesc",String(120))
    path = Column("imagepath",String(120))
    isdefault = Column("isdefault",Integer)
    istopshow = Column("istopshow",Integer)
    isenable = Column("isenable",Integer)
    sortindex = Column("sortindex",Integer)
    cat = Column("category",String(1))

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

class Show(db.Model):

    __tablename__ = 'Shows'

    id = Column("showid",Integer, primary_key=True)
    catid = Column("catid",Integer)
    catname =Column("catname",String(128))
    name = Column("showname",String(120), unique=True)
    desc = Column("showdesc",String(1024))
    addr = Column("addr",String(128))
    features = Column("features",String(1024))
    phone = Column("phone",String(32))
    intro = Column("intro",String(1024))
    begindate = Column("begindate",String(64))
    enddate = Column("enddate",String(64))
    price = Column("price",Numeric(10,2))
    maxprice = Column("maxprice",Numeric(10,2))
    provid = Column("provid",Integer)
    provname = Column("provname",String(128))
    cityid = Column("cityid",Integer)
    cityname = Column("cityname",String(128))
    districtid = Column("districtid",Integer)
    districtname = Column("districtname",String(128))
    duration = Column("duration",String(32))
    sortindex = Column("sortindex",Integer)
    img = Column("img",String(126))
    thumb = Column("thumb",String(126))
    isbest = Column("isbest",Integer)
    isnew = Column("isnew",Integer)
    ishot = Column("ishot",Integer)
    istopshow = Column("istopshow",Integer)

    lon = Column("lon",String(64))
    lat = Column("lat",String(64))
    cbdname = Column("cbdname",String(126))
    cbdid = Column("cbdid",Integer)
 
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
            'begindate':self.begindate,
            'enddate':self.enddate,
            'name': self.name,
            'desc':self.desc,
            'addr': self.addr,
            'features':self.features,
            'phone': self.phone,
            'intro': self.intro,
            'price':self.price,
            'maxprice':self.maxprice,
            'provid':self.provid,
            'provname':self.provname,
            'cityid':self.cityid,
            'cityname':self.cityname,
            'districtid':self.districtid,
            'districtname':self.districtname,
            'duration': self.duration,
            'sortindex':self.sortindex,
            'img': self.img,
            'thumb': self.thumb,
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            'lon':self.lon,#经度
            "lat":self.lat,#维度
            "cbdname":self.cbdname, #商圈名称
            "cbdid":self.cbdid,#商圈标识
            }
                
        return data

class ShowGallery(db.Model):
    __tablename__ = 'showgalleries'
    id = Column("galleryid",Integer, primary_key=True)
    objid=Column("showid",Integer)
    title = Column("imagetitle",String(120))
    desc = Column("imagedesc",String(120))
    path = Column("imagepath",String(120))
    isdefault = Column("isdefault",Integer)
    istopshow = Column("istopshow",Integer)
    isenable = Column("isenable",Integer)
    sortindex = Column("sortindex",Integer)
    cat = Column("category",String(1))

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

class Training(db.Model):

    __tablename__ = 'Trainings'

    id = Column("trainingid",Integer, primary_key=True)
    catid = Column("catid",Integer)
    catname =Column("catname",String(128))
    name = Column("trainingname",String(120), unique=True)
    desc = Column("trainingdesc",String(1024))
    team = Column("team",String(1024))
    content = Column("trainingcontent",String(1024))
    addr = Column("addr",String(128))
    features = Column("features",String(1024))
    phone = Column("phone",String(32))
    intro = Column("intro",String(1024))
    begindate = Column("begindate",String(64))
    enddate = Column("enddate",String(64))
    price = Column("price",Numeric(10,2))
    originalprice = Column("originalprice",Numeric(10,2))
    provid = Column("provid",Integer)
    provname = Column("provname",String(128))
    cityid = Column("cityid",Integer)
    cityname = Column("cityname",String(128))
    districtid = Column("districtid",Integer)
    districtname = Column("districtname",String(128))
    duration = Column("duration",String(32))
    sortindex = Column("sortindex",Integer)
    img = Column("img",String(126))
    thumb = Column("thumb",String(126))
    isbest = Column("isbest",Integer)
    isnew = Column("isnew",Integer)
    ishot = Column("ishot",Integer)
    istopshow = Column("istopshow",Integer)
    lon = Column("lon",String(64))
    lat = Column("lat",String(64))
    cbdname = Column("cbdname",String(126))
    cbdid = Column("cbdid",Integer)
 
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
            'begindate':self.begindate,
            'enddate':self.enddate,
            'name': self.name,
            'content':self.content,
            'desc':self.desc,
            'addr': self.addr,
            'team':self.team,
            'features':self.features,
            'phone': self.phone,
            'intro': self.intro,
            'price':self.price,
            'originalprice':self.originalprice,
            'provid':self.provid,
            'provname':self.provname,
            'cityid':self.cityid,
            'cityname':self.cityname,
            'districtid':self.districtid,
            'districtname':self.districtname,
            'duration': self.duration,
            'sortindex':self.sortindex,
            'img': self.img,
            'thumb': self.thumb,
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            'lon':self.lon,#经度
            "lat":self.lat,#维度
            "cbdname":self.cbdname, #商圈名称
            "cbdid":self.cbdid,#商圈标识
            }
                
        return data

class TrainingGallery(db.Model):
    __tablename__ = 'traininggalleries'
    id = Column("galleryid",Integer, primary_key=True)
    objid=Column("trainingid",Integer)
    title = Column("imagetitle",String(120))
    desc = Column("imagedesc",String(120))
    path = Column("imagepath",String(120))
    isdefault = Column("isdefault",Integer)
    istopshow = Column("istopshow",Integer)
    isenable = Column("isenable",Integer)
    cat = Column("category",String(1))
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





class TrainingClass(db.Model):

    __tablename__ = 'TrainingClasses'

    id = Column("classid",Integer, primary_key=True)
    trainingid = Column("trainingid",Integer)
    name = Column("classname",String(120), unique=True)
    desc = Column("classdesc",String(1024))
    content = Column("classcontent",String(1024))
    features = Column("features",String(1024))
    
    intro = Column("intro",String(1024))
    begindate = Column("begindate",String(64))
    enddate = Column("enddate",String(64))
    price = Column("price",Numeric(10,2))
    originalprice = Column("originalprice",Numeric(10,2))
    
    duration = Column("duration",String(32))
    sortindex = Column("sortindex",Integer)
    img = Column("img",String(126))
    thumb = Column("thumb",String(126))
    isbest = Column("isbest",Integer)
    isnew = Column("isnew",Integer)
    ishot = Column("ishot",Integer)
    istopshow = Column("istopshow",Integer)
   
 
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
            'price':self.price,
            'originalprice':self.originalprice,
            
            'duration': self.duration,
            'sortindex':self.sortindex,
            'img': self.img,
            'thumb': self.thumb,
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            
            }
                
        return data

class TrainingClassGallery(db.Model):
    __tablename__ = 'TrainingClassGalleries'
    id = Column("galleryid",Integer, primary_key=True)
    objid=Column("trainingclassid",Integer)
    title = Column("imagetitle",String(120))
    desc = Column("imagedesc",String(120))
    path = Column("imagepath",String(120))
    cat = Column("category",String(1))
    isdefault = Column("isdefault",Integer)
    istopshow = Column("istopshow",Integer)
    isenable = Column("isenable",Integer)
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



class Lecturer(db.Model):

    __tablename__ = 'Lecturers'

    id = Column("lecturerid",Integer, primary_key=True)
    catid = Column("catid",Integer)
    catname =Column("catname",String(128))
    name = Column("lecturername",String(120), unique=True)
    desc = Column("lecturerdesc",String(1024))
    team = Column("team",String(1024))
    content = Column("lecturercontent",String(1024))
    addr = Column("addr",String(128))
    features = Column("features",String(1024))
    phone = Column("phone",String(32))
    intro = Column("intro",String(1024))
    begindate = Column("begindate",String(64))
    enddate = Column("enddate",String(64))
    price = Column("price",Numeric(10,2))
    provid = Column("provid",Integer)
    provname = Column("provname",String(128))
    cityid = Column("cityid",Integer)
    cityname = Column("cityname",String(128))
    districtid = Column("districtid",Integer)
    districtname = Column("districtname",String(128))
    duration = Column("duration",String(32))
    sortindex = Column("sortindex",Integer)
    img = Column("img",String(126))
    avatar = Column("avatar",String(126))
    thumb = Column("thumb",String(126))
    isbest = Column("isbest",Integer)
    isnew = Column("isnew",Integer)
    ishot = Column("ishot",Integer)
    istopshow = Column("istopshow",Integer)
    lon = Column("lon",String(64))
    lat = Column("lat",String(64))
    cbdname = Column("cbdname",String(126))
    cbdid = Column("cbdid",Integer)
    title = Column("title",String(126))
    
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
            'begindate':self.begindate,
            'enddate':self.enddate,
            'name': self.name,
            'content':self.content,
            'desc':self.desc,
            'addr': self.addr,
            'team':self.team,
            'features':self.features,
            'phone': self.phone,
            'intro': self.intro,
            'price':self.price,
            'provid':self.provid,
            'provname':self.provname,
            'cityid':self.cityid,
            'cityname':self.cityname,
            'districtid':self.districtid,
            'districtname':self.districtname,
            'duration': self.duration,
            'sortindex':self.sortindex,
            'img': self.img,
            'thumb': self.thumb,
            'isbest': self.isbest,
            'isnew':self.isnew,
            'ishot':self.ishot,
            'istopshow':self.istopshow,
            'lon':self.lon,#经度
            "lat":self.lat,#维度
            "cbdname":self.cbdname, #商圈名称
            "cbdid":self.cbdid,#商圈标识
            "title":self.title
            }
                
        return data

class LecturerGallery(db.Model):
    __tablename__ = 'lecturergalleries'
    id = Column("galleryid",Integer, primary_key=True)
    objid=Column("trainingid",Integer)
    title = Column("imagetitle",String(120))
    desc = Column("imagedesc",String(120))
    path = Column("imagepath",String(120))
    isdefault = Column("isdefault",Integer)
    istopshow = Column("istopshow",Integer)
    isenable = Column("isenable",Integer)
    cat = Column("category",String(1))
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
