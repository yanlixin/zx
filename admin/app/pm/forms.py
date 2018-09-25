from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField,HiddenField,PasswordField,SelectField,BooleanField
from wtforms.validators import Length,DataRequired,Email
import uuid

class ProjectForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    no = TextField('No', id='txt_no' ,validators=[DataRequired(message='编号不能为空')])
    name = TextField('Name', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    fullname = TextField('FullName', id='txt_fullname' ,validators=[DataRequired(message='全称不能为空')])
    desc = TextAreaField('Desc', id='txt_desc')
    
class TaskForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    projid = HiddenField('ProjectId', id='txt_projid')
    pid = SelectField('TaskPId' ,id='txt_pid', coerce=str)
    no = TextField('TaskNo', id='txt_no' ,validators=[DataRequired(message='编号不能为空')])
    name = TextField('TaskName', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    desc = TextAreaField('TaskDesc', id='txt_desc' )
    memo = TextAreaField('Memo', id='txt_memo' )
    isendnode = BooleanField('IsEndNode', id='txt_isendnode')
    #isendnode = SelectField('IsEndNode', id='txt_isendnode',choices=[('False', '否'),('True', '是'), ])

class ActivityForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    projid = HiddenField('ProjectId', id='txt_projid')
    taskid = HiddenField('TaskId' ,id='txt_taskid')
    phaseid = SelectField('PhaseID' ,id='txt_phaseid', coerce=str,validators=[DataRequired(message='项目阶段不能为空')])
    no = TextField('ActivityNo', id='txt_no' ,validators=[DataRequired(message='编号不能为空')])
    name = TextField('ActivityName', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    desc = TextAreaField('ActivityDesc', id='txt_desc' )
    memo = TextAreaField('Memo', id='txt_memo' )
    hasdeliverables = BooleanField('HasDeliverables', id='txt_hasdeliverables')
    #isendnode = SelectField('IsEndNode', id='txt_isendnode',choices=[('False', '否'),('True', '是'), ])

class DocForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    projid = HiddenField('ProjectId', id='txt_projid')
    catid = SelectField('Catid' ,id='txt_catid', coerce=str)
    no = TextField('DocNo', id='txt_no' ,validators=[DataRequired(message='编号不能为空')])
    title = TextField('Title', id='txt_title' ,validators=[DataRequired(message='名称不能为空')])
    fullname = TextField('FullName', id='txt_fullname' ,validators=[DataRequired(message='全称不能为空')])
    alias = TextAreaField('Alias', id='txt_alias' )
    desc = TextAreaField('Desc', id='txt_desc' )
    memo = TextAreaField('Memo', id='txt_memo' )
    summary = TextAreaField('Summary', id='txt_summary' )


class DocCatForm(FlaskForm):
    id = HiddenField('Id', id='txt_id')
    projid = HiddenField('ProjectId', id='txt_projid')
    no = TextField('No', id='txt_no' ,validators=[DataRequired(message='编号不能为空')])
    name = TextField('Name', id='txt_name' ,validators=[DataRequired(message='名称不能为空')])
    isrequired = BooleanField('IsRequired', id='txt_IsRequired')
    desc = TextAreaField('Desc', id='txt_desc')

    