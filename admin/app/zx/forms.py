from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,HiddenField,TextAreaField,SelectField



class SchoolForm(FlaskForm):
    name = TextField('Name', id='Name')
    desc = TextField('desc', id='desc')
    addr = TextField('addr', id='addr')
    tuition = TextField('tuition', id='tuition')
    features = TextField('features', id='features')
    phone = TextField('phone', id='phone')
    intro = TextField('intro', id='intro')
    team = TextField('team', id='team')
    founded = TextField('founded', id='founded')
    age = TextField('age', id='age')
    scale = TextField('scale', id='scale')
    population = TextField('population', id='population')
    foreignduration = TextField('foreignduration', id='foreignduration')
    schoolbus = TextField('schoolbus', id='schoolbus')
    schoolbus = TextField('cramclass', id='cramclass')
    # 'districtid' INTEGER DEFAULT NULL,

class CatForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    name = TextField('Name', id='txt_name')
    desc = TextAreaField('desc', id='txt_desc')
    typeid = SelectField('typeid' ,id='txt_typeid',choices=[('1', '学校'), ('2', '课余'), ('3', '培训机构'),('4', '明星讲师')])
    typename = HiddenField('typename', id='txt_typename')
    #pid = SelectField('TaskPId' ,id='txt_pid', coerce=str)

class CBDForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    name = TextField('Name', id='txt_name')
    desc = TextAreaField('desc', id='txt_desc')
    distid = SelectField('distid' ,id='txt_distid', coerce=str)