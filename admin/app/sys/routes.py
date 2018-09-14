import sys,os,logging, json,uuid
from sqlalchemy import and_,or_
from flask import render_template,request,make_response
from flask_login import login_required
from wtforms.validators import ValidationError
from datatables import DataTable

from app.sys import blueprint
from app import db,uploaded_photos,base_path
from app.base.sysmodels import Role,UserRole,Permissions,PermissionRole
from app.base.perms import permission_required,admin_required
from app.base.models import User,District,Grade,Category,Province,City
from .forms import RoleForm

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')


@blueprint.route('/manager/jsondata', methods=['GET', 'POST'])
@login_required
#@admin_required
def manager_jsondata():
    table = DataTable(request.args, User, User.query, [
        "id",
        "username",
        "email",
        "password"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))

    return json.dumps(table.json())


@blueprint.route('/perm/jsondata', methods=['GET', 'POST'])
@login_required
def perm_jsondata():
    table = DataTable(request.args, Permission, Permission.query, [
        "id",
        "name",
        "desc",
        "sortindex"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))

    return json.dumps(table.json())

@blueprint.route('/role/list', methods=['GET'])
@login_required
def role_list():
     return render_template(
            'rolelist.html',
        )

@blueprint.route('/role/data', methods=['GET', 'POST'])
@login_required
def role_jsondata():
    table = DataTable(request.args, Role, Role.query, [
        "id",
        "name",
        "desc",
        "status_text"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    table.searchable(lambda qs, sq: qs.filter(or_(Role.name.contains(sq) , Role.desc.contains(sq))))
    return json.dumps(table.json())

@blueprint.route('/role/edit', methods=['GET'])
@login_required
def role_edit(roleid):
    print(roleid)
    id = request.args.get('id', -1, type=int)
    role = Role.query.get(id)
    if role==None:
        role = Role(id=0)
    roleForm=RoleForm(obj=role)
    return render_template(
            'roleedit.html',
            form=roleForm,
        )

@blueprint.route('/role/save', methods=['POST'])
@login_required
def role_save():
    form = RoleForm(**request.form)
    result='OK'
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        role = Role()
        form.populate_obj(role)
        if int(role.id)>0:
            role.id=int(role.id)
            role.mark_add(1)
            o=db.session.query(Role).filter_by(id=role.id)
            o.update(role.to_dict() )
        else:
            role.id=None
            role.mark_add(0)
            db.session.add(role)
        db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


@blueprint.route('/role/delete', methods=['POST'])
@login_required
def role_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    obj=db.session.query(Role).filter_by(id=id)
    obj.update(obj.first().mark_del(0) )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


