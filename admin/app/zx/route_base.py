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
from app.base.models import UUID_DEF
from app.pm.models.model_base import ProjectType,Phase,ActivityCode
from app.pm.forms.form_base import TypeForm,PhaseForm,ActivityCodeForm

@blueprint.route('/basic/type/list', methods=['GET'])
@login_required
def type_list():
    return render_template('basic/typelist.html')

@blueprint.route('/basic/type/data', methods=['GET', 'POST'])
@login_required
def type_jsondata():
    table = DataTable(request.args, ProjectType, ProjectType.query, [
        "id",
        "name",
        "desc",
        "status_text"
    ])
    table.searchable(lambda qs, sq: qs.filter(or_(ProjectType.name.contains(sq) , ProjectType.desc.contains(sq))))
    return json.dumps(table.json())

@blueprint.route('/basic/type/edit', methods=['GET'])
@login_required
def type_edit():
    id = request.args.get('id', UUID_DEF)
    obj = ProjectType.query.get(id)
    if obj==None:
        obj = ProjectType(id=UUID_DEF)

    
    form=TypeForm(obj=obj)
    return render_template(
            'basic/typeedit.html',
            form=form,
        )

@blueprint.route('/basic/type/save', methods=['POST'])
@login_required
def type_save():
    form = TypeForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = ProjectType()
        form.populate_obj(obj)
        if obj.id==UUID_DEF:
            obj.id=None
            obj.mark_add()
            db.session.add(obj)
        else:
            obj.id=obj.id
            obj.mark_update()
            o=db.session.query(ProjectType).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })




@blueprint.route('/basic/phase/list', methods=['GET'])
@login_required
def phase_list():
    return render_template('basic/phaselist.html')

@blueprint.route('/basic/phase/data', methods=['GET', 'POST'])
@login_required
def phase_jsondata():
    table = DataTable(request.args, Phase, Phase.query, [
        "id",
        "no",
        "name",
        "desc",
        "status_text"
    ])
    table.searchable(lambda qs, sq: qs.filter(or_(Phase.name.contains(sq) ,Phase.no.contains(sq) , Phase.desc.contains(sq))))
    return json.dumps(table.json())

@blueprint.route('/basic/phase/edit', methods=['GET'])
@login_required
def phase_edit():
    id = request.args.get('id', UUID_DEF)
    obj = Phase.query.get(id)
    if obj==None:
        obj = Phase(id=UUID_DEF)

    
    form=PhaseForm(obj=obj)
    form.projtypeid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in ProjectType.query.all()]
    if list != None and len(list)>0:
        form.projtypeid.choices=form.projtypeid.choices+list
    return render_template(
            'basic/phaseedit.html',
            form=form,
        )

@blueprint.route('/basic/phase/save', methods=['POST'])
@login_required
def phase_save():
    form = PhaseForm(**request.form)
    form.projtypeid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in ProjectType.query.all()]
    if list != None and len(list)>0:
        form.projtypeid.choices=form.projtypeid.choices+list
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Phase()
        form.populate_obj(obj)
        if obj.id==UUID_DEF:
            obj.id=None
            print(obj.projtypeid)
            obj.mark_add()
            db.session.add(obj)
        else:
            obj.id=obj.id
            obj.mark_update()
            o=db.session.query(Phase).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })

@blueprint.route('/basic/phase/delete', methods=['POST'])
@login_required
def phase_del():
    id = request.args.get('id')
    result='OK'
    msg=''
    obj=db.session.query(Phase).filter_by(id=id)
    obj.update(obj.first().mark_del() )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


##


@blueprint.route('/basic/activitycode/list', methods=['GET'])
@login_required
def activitycode_list():
    return render_template('basic/activitycodelist.html')

@blueprint.route('/basic/activitycode/data', methods=['GET', 'POST'])
@login_required
def activitycode_jsondata():
    table = DataTable(request.args, ActivityCode, ActivityCode.query, [
        "id",
        "no",
        "name",
        "desc",
        "status_text"
    ])
    table.searchable(lambda qs, sq: qs.filter(or_(ActivityCode.name.contains(sq) , ActivityCode.no.contains(sq) ,ActivityCode.desc.contains(sq))))
    return json.dumps(table.json())

@blueprint.route('/basic/activitycode/edit', methods=['GET'])
@login_required
def activitycode_edit():
    id = request.args.get('id', UUID_DEF)
    obj = ActivityCode.query.get(id)
    if obj==None:
        obj = ActivityCode(id=UUID_DEF)

    
    form=ActivityCodeForm(obj=obj)
    form.projtypeid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in ProjectType.query.all()]
    if list != None and len(list)>0:
        form.projtypeid.choices=form.projtypeid.choices+list
    return render_template(
            'basic/activitycodeedit.html',
            form=form,
        )

@blueprint.route('/basic/activitycode/save', methods=['POST'])
@login_required
def activitycode_save():
    form = ActivityCodeForm(**request.form)
    form.projtypeid.choices = [('','--select--')]
    list=[(str(g.id), g.name) for g in ProjectType.query.all()]
    if list != None and len(list)>0:
        form.projtypeid.choices=form.projtypeid.choices+list
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = ActivityCode()
        form.populate_obj(obj)
        if obj.id==UUID_DEF:
            obj.id=None
            
            obj.mark_add()
            db.session.add(obj)
        else:
            obj.id=obj.id
            obj.mark_update()
            o=db.session.query(ActivityCode).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })

@blueprint.route('/basic/activitycode/delete', methods=['POST'])
@login_required
def activitycode_del():
    id = request.args.get('id')
    result='OK'
    msg=''
    obj=db.session.query(ActivityCode).filter_by(id=id)
    obj.update(obj.first().mark_del() )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })