from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField,HiddenField,PasswordField
from wtforms.validators import Length,DataRequired,Email


class ProjectForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    no = TextField('No', id='txt_no' ,validators=[DataRequired(message='编号不能为空')])
    name = TextField('Name', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    fullname = TextField('FullName', id='txt_fullname' ,validators=[DataRequired(message='全称不能为空')])
    desc = TextAreaField('Desc', id='txt_desc')
    
