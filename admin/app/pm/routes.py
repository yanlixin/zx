from app.pm import blueprint
import sys,os,logging, json,uuid
from sqlalchemy import and_,or_
from flask import render_template,request,make_response,jsonify
from flask_login import login_required,current_user
from wtforms.validators import ValidationError
from datatables import DataTable
from datetime import datetime 


from app import db,uploaded_photos,base_path
from .models import UUID_DEF,Project,Deliverable,TeamMember,Doc
from .forms import ProjectForm
from .doc_routes import *
from .wbs_routes import *
from .basic_routes import *

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')

@blueprint.route('/project/list', methods=['GET'])
@login_required
def project_list():
    return render_template('Projectlist.html')

@blueprint.route('/project/data', methods=['GET', 'POST'])
@login_required
def project_jsondata():
    table = DataTable(request.args, Project, Project.query, [
        "id",
        "no",
        "name",
        "fullname",
        "desc",
        "status_text"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))
    table.searchable(lambda qs, sq: qs.filter(or_(Project.no.contains(sq) , Project.name.contains(sq), Project.desc.contains(sq))))
    return json.dumps(table.json(),)
    #return jsonify(table)

@blueprint.route('/project/edit', methods=['GET'])
@login_required
def project_edit():
    id = request.args.get('id', UUID_DEF)
    obj = Project.query.get(id)
    if obj==None:
        obj = Project(id=UUID_DEF)
    form=ProjectForm(obj=obj)
    return render_template(
            'projectedit.html',
            form=form,
        )

@blueprint.route('/project/view', methods=['GET'])
@login_required
def project_view():
    id = request.args.get('id', UUID_DEF)
    obj = Project.query.get(id)
    if obj==None:
        obj = Project(id=UUID_DEF)
    form={"id":obj.id,"name":obj.name,"desc":obj.desc,"fullname":obj.fullname}
    return render_template(
            'projectview.html',
            proj=form,
        )

@blueprint.route('/project/save', methods=['POST'])
@login_required
def project_save():
    form = ProjectForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Project()
        form.populate_obj(obj)
        obj.extradata={
    "description": "Super Poodle",
    "sale_price": 179.99,
    "animal_info": {
        "weight": 25,
        "fur_color": "white",
        "eye_color": "green"
    }
}
        if obj.id==UUID_DEF:
            obj.id=None
            obj.mark_add()
            db.session.add(obj)
        else:
            obj.id=obj.id
        
            obj.mark_update()
            o=db.session.query(Project).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })



@blueprint.route('/deliverable/data', methods=['GET', 'POST'])
@login_required
def deliverable_jsondata():
    table = DataTable(request.args, Deliverable, Deliverable.query, [
        "id",
        "name",
        "desc",
        "status_text"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))
    table.searchable(lambda qs, sq: qs.filter(or_( Deliverable.name.contains(sq), Deliverable.desc.contains(sq))))
    return json.dumps(table.json(),)
    #return jsonify(table)

@blueprint.route('/wbs/data', methods=['GET', 'POST'])
@login_required
def wbs_jsondata():
    json=[
        {
        "id": 1,
        "pid": 0,
        "status": 1,
        "name": "系统管理",
        "permissionValue": "open:system:get"
        },
        {
        "id": 2,
        "pid": 0,
        "status": 1,
        "name": "字典管理",
        "permissionValue": "open:dict:get"
        },
        {
        "id": 20,
        "pid": 1,
        "status": 1,
        "name": "新增系统",
        "permissionValue": "open:system:add"
        },
        {
        "id": 21,
        "pid": 1,
        "status": 1,
        "name": "编辑系统",
        "permissionValue": "open:system:edit"
        },
        {
        "id": 22,
        "pid": 1,
        "status": 1,
        "name": "删除系统",
        "permissionValue": "open:system:delete"
        },
        {
        "id": 33,
        "pid": 2,
        "status": 1,
        "name": "系统环境",
        "permissionValue": "open:env:get"
        },
        {
        "id": 333,
        "pid": 33,
        "status": 1,
        "name": "新增环境",
        "permissionValue": "open:env:add"
        },
        {
        "id": 3333,
        "pid": 33,
        "status": 1,
        "name": "编辑环境",
        "permissionValue": "open:env:edit"
        },
        {
        "id": 233332,
        "pid": 33,
        "status": 0,
        "name": "删除环境",
        "permissionValue": "open:env:delete"
        }
    ]
   #return json.dumps(table.json(),)
    return jsonify(json)