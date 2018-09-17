from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField,HiddenField,PasswordField
from wtforms.validators import Length,DataRequired,Email


class RoleForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    name = TextField('Name', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    desc = TextAreaField('Desc', id='txt_desc')
    sortindex = TextField('sortindex', id='txt_sortindex')
class PermissionForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    name = TextField('Name', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    desc = TextAreaField('Desc', id='txt_desc')
    group = TextField('group', id='txt_group',validators=[DataRequired(message='分组不能为空')])

class ManagerForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    displayname = TextField('displayname', id='txt_displayname' ,validators=[DataRequired(message='用户名称不能为空')])
    loginname = TextField('loginname', id='txt_loginname' ,validators=[DataRequired(message='登录名称不能为空')])
    password = PasswordField('password', id='txt_password' ,validators=[])
    email = TextField('email', id='txt_email' ,validators=[])
    mobile = TextField('mobile', id='txt_mobile' ,validators=[])
    desc = TextAreaField('Desc', id='txt_desc')
    sortindex = TextField('sortindex', id='txt_sortindex')

class ManagerRoleForm(FlaskForm):
    id = HiddenField('Id', id='txt_id',validators=[DataRequired(message='用户不能为空')])
    roleids=HiddenField('roleids', id='txt_roleids',validators=[DataRequired(message='角色不能为空')])