from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField,HiddenField
from wtforms.validators import Length,DataRequired


class RoleForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    name = TextField('Name', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    desc = TextAreaField('Desc', id='txt_desc')
    sortindex = TextField('sortindex', id='txt_sortindex')
