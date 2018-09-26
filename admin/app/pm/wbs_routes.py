from app.pm import blueprint
import sys,os,logging, json,uuid
from sqlalchemy import and_,or_
from flask import render_template,request,make_response,jsonify
from flask_login import login_required,current_user
from wtforms.validators import ValidationError
from datatables import DataTable
from datetime import datetime 


from app import db,uploaded_photos,base_path
from app.base.sysmodels import User
from .models import UUID_DEF,Task,Activity,Deliverable,ActivityDeliverable,DocCat,Phase,ActivityCode
from .forms import TaskForm,ActivityForm,DeliverableForm

@blueprint.route('/wbs/task/list', methods=['GET'])
@login_required
def task_list():
    projid = request.args.get('projectid', UUID_DEF)
    return render_template('wbs/tasklist.html',projid=projid)

@blueprint.route('/wbs/task/data', methods=['GET', 'POST'])
@login_required
def task_jsondata():
    projid = request.args.get('projectid', UUID_DEF)
    result =[item for item  in Task.tree(projid)]
    return json.dumps(result)

@blueprint.route('/wbs/task/edit', methods=['GET'])
@login_required
def task_edit():
    id = request.args.get('id', UUID_DEF)
    projid=request.args.get('projid')
    pid=request.args.get('pid', UUID_DEF)
    obj = Task.query.get(id)
    if obj==None:
        obj = Task(id=UUID_DEF,projid=projid)

    if pid!=UUID_DEF:
        obj.pid=pid
    form=TaskForm(obj=obj)
    #form.pid.choices = [(str(g.id), g.name) for g in Task.query.order_by('TaskName')]
    form.pid.choices = [(UUID_DEF,'--select--')]
    list=[(str(g.id), g.name) for g in Task.query.order_by('TaskName')]
    print(list)
    if list != None and len(list)>0:
        form.pid.choices=form.pid.choices+list
    #form.pid.choices = [(str(g.id), g.name) for g in DocCat.query.order_by('CatName')]
    return render_template(
            'wbs/taskedit.html',
            form=form,
        )

@blueprint.route('/wbs/task/save', methods=['POST'])
@login_required
def task_save():
    form = TaskForm(**request.form)
    form.pid.choices = [(UUID_DEF,'--select--')]
    list=[(str(g.id), g.name) for g in Task.query.order_by('TaskName')]
    if list != None and len(list)>0:
        form.pid.choices=form.pid.choices+list
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Task()
        form.populate_obj(obj)
        if obj.id==UUID_DEF:
            obj.id=None
            obj.mark_add()
            db.session.add(obj)
        else:
            obj.id=obj.id
            if obj.pid==UUID_DEF:
                obj.pid=None
            obj.mark_update()
            o=db.session.query(Task).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })



@blueprint.route('/wbs/act/edit', methods=['GET'])
@login_required
def act_edit():
    id = request.args.get('id', UUID_DEF)
    projid=request.args.get('projid')
    taskid=request.args.get('taskid')
    obj = Activity.query.get(id)
    if obj==None:
        obj = Activity(id=UUID_DEF,projid=projid,taskid=taskid)
    form=ActivityForm(obj=obj)
    form.phaseid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in Phase.select()]
    if list != None and len(list)>0:
        form.phaseid.choices=form.phaseid.choices+list
    
    form.actcodeid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in ActivityCode.select()]
    if list != None and len(list)>0:
        form.actcodeid.choices=form.actcodeid.choices+list
    return render_template(
            'wbs/actedit.html',
            form=form,
        )

@blueprint.route('/wbs/act/save', methods=['POST'])
@login_required
def act_save():
    form = ActivityForm(**request.form)
    form.phaseid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in Phase.select()]
    if list != None and len(list)>0:
        form.phaseid.choices=form.phaseid.choices+list
    
    form.actcodeid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in ActivityCode.select()]
    if list != None and len(list)>0:
        form.actcodeid.choices=form.actcodeid.choices+list

    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Activity()
        form.populate_obj(obj)
        if obj.id==UUID_DEF:
            obj.id=None
            obj.mark_add()
            db.session.add(obj)
        else:
            obj.id=obj.id
            obj.mark_update()
            o=db.session.query(Activity).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })

@blueprint.route('/wbs/deli/edit', methods=['GET'])
@login_required
def act_deli_edit():
    id = request.args.get('id', UUID_DEF)
    projid=request.args.get('projid')
    actid=request.args.get('actid')
    obj = Deliverable.query.get(id)
    if obj==None:
        obj = Deliverable(id=UUID_DEF,projid=projid)
    form=DeliverableForm(obj=obj)
    form.actid.data=actid
    return render_template(
            'wbs/delidit.html',
            form=form,
        )

@blueprint.route('/wbs/deli/save', methods=['POST'])
@login_required
def act_deli_save():
    form = DeliverableForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Deliverable()
        form.populate_obj(obj)
        if obj.id==UUID_DEF:
            obj.id=Deliverable.gen_id()
            obj.mark_add()
            db.session.add(obj)
            db.session.commit()
            adobj=ActivityDeliverable()
            form.populate_obj(adobj)
            adobj.deliid=obj.id
            adobj.mark_add()
            db.session.add(adobj)
        else:
            obj.id=obj.id
            obj.mark_update()
            o=db.session.query(Deliverable).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })
