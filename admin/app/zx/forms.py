from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField



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
