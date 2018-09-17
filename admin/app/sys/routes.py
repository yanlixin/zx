import sys,os,logging, json,uuid
from sqlalchemy import and_,or_
from flask import render_template,request,make_response,jsonify
from flask_login import login_required,current_user
from wtforms.validators import ValidationError
from datatables import DataTable
from datetime import datetime 

from app.sys import blueprint
from app import db,uploaded_photos,base_path
from app.base.sysmodels import User,Role,UserRole,Permission,PermissionRole
from app.base.perms import permission_required,admin_required
from app.base.models import District,Grade,Category,Province,City
from .forms import RoleForm,ManagerForm,ManagerRoleForm,PermissionForm,RolePermissionForm

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')

@blueprint.route('/manager/list', methods=['GET'])
@login_required
@admin_required
def manager_list():
    return render_template('managerlist.html')

@blueprint.route('/manager/data', methods=['GET', 'POST'])
@login_required
@admin_required
def manager_jsondata():
    table = DataTable(request.args, User, User.query, [
        "id",
        "displayname",
        "loginname",
        "email",
        "mobile",
        "desc",
        "status_text"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))
    table.searchable(lambda qs, sq: qs.filter(or_(User.displayname.contains(sq) , User.loginname.contains(sq), User.email.contains(sq), User.mobile.contains(sq))))
    return json.dumps(table.json())

@blueprint.route('/manager/edit', methods=['GET'])
@login_required
@admin_required
def manager_edit():
    id = request.args.get('id', -1, type=int)
    manager = User.query.get(id)
    if manager==None:
        manager = User(id=0)
    form=ManagerForm(obj=manager)
    return render_template(
            'manageredit.html',
            form=form,
        )

@blueprint.route('/manager/save', methods=['POST'])
@login_required
@admin_required
def manager_save():
    form = ManagerForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = User()
        form.populate_obj(obj)
        if int(obj.id)>0:
            obj.id=int(obj.id)
            obj.mark_update()
            o=db.session.query(User).filter_by(id=obj.id)
            if o.first().ismaster==1:
                 valid=False
                 msg=["不能修改系统默认用户"]
            else :
                o.update(obj.to_dict() )
                if form.password.data!="":
                    pwd=o.first().gen_password(form.password.data)
                    o.update({'password':pwd})
        else:
            if form.password.data=="":
                 valid=False
                 msg=["用户密码不能为空"]
            else:
                obj.id=None
                obj.gen_password(form.password.data)
                obj.mark_add()
                db.session.add(obj)
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })

@blueprint.route('/manager/delete', methods=['POST'])
@login_required
@admin_required
def manager_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    obj=db.session.query(User).filter_by(id=id)
    if obj.first().ismaster==1:
        valid=False
        msg=["不能删除系统默认用户"]
    obj.update(obj.first().mark_del() )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })



@blueprint.route('/role/list', methods=['GET'])
@login_required
@admin_required
def role_list():
    return render_template('rolelist.html',)

@blueprint.route('/role/data', methods=['GET', 'POST'])
@login_required
@admin_required
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
@admin_required
def role_edit():
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
@admin_required
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
            role.mark_add()
            o=db.session.query(Role).filter_by(id=role.id)
            o.update(role.to_dict() )
        else:
            role.id=None
            role.mark_add()
            db.session.add(role)
        db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


@blueprint.route('/role/delete', methods=['POST'])
@login_required
@admin_required
def role_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    obj=db.session.query(Role).filter_by(id=id)
    obj.update(obj.first().mark_del() )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


@blueprint.route('/managerrole/edit', methods=['GET'])
@login_required
@admin_required
def managerrole_edit():
    id = request.args.get('id', -1, type=int)
    roles = Role.query.all()
    # if manager==None:
    #     manager = User(id=0)
    userRoles=UserRole.select().filter_by(managerid=id).all()

    form=ManagerRoleForm(id=id)
    list=[]
    
    for role in roles:
        obj ={'id':role.id,'name':role.name,'selected':False}
        for ur in userRoles:
            if ur.roleid==role.id:
                obj['selected']=True
                break
        list.append(obj)

    return render_template(
            'managerroleedit.html',
            form=form,
            roles=list,
        )
@blueprint.route('/managerrole/save', methods=['POST'])
@login_required
@admin_required
def manager_role_save():
    form = ManagerRoleForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        id=form.id.data
        roleids=form.roleids.data
        UserRole.write_data(id,roleids)
    return json.dumps({'valid':valid,'result':result,'msg':msg })


@blueprint.route('/perm/list', methods=['GET'])
@login_required
@admin_required
def perm_list():
    return render_template('permlist.html',)

@blueprint.route('/perm/data', methods=['GET', 'POST'])
@login_required
@admin_required
def perm_jsondata():
    table = DataTable(request.args, Permission, Permission.query, [
        "id",
        "name",
        "desc",
        "group",
        "uuid"
    ])
    table.searchable(lambda qs, sq: qs.filter(or_(Permission.name.contains(sq) , Permission.desc.contains(sq))))
    return json.dumps(table.json())

@blueprint.route('/perm/edit', methods=['GET'])
@login_required
@admin_required
def perm_edit():
    id = request.args.get('id', -1, type=int)
    obj = Permission.query.get(id)
    if obj==None:
        obj = Permission(id=0)
    form=PermissionForm(obj=obj)
    return render_template(
            'permedit.html',
            form=form,
        )
@blueprint.route('/perm/save', methods=['POST'])
@login_required
@admin_required
def perm_save():
    form = PermissionForm(**request.form)
    result='OK'
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Permission()
        form.populate_obj(obj)
        if int(obj.id)>0:
            obj.id=int(obj.id)
            o=db.session.query(Permission).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        else:
            obj.id=None
            obj.uuid=str(uuid.uuid1())

            obj.createdbydate=datetime.now()
            obj.createdbymanagerid=current_user.id
            db.session.add(obj)
        db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/roleperm/list', methods=['GET'])
@login_required
@admin_required
def role_perm_list():
    roles = Role.select()
    permission=Permission.select().all()
    rolePermission=PermissionRole.select().filter_by(roleid=roles.first().id).all()

    form=RolePermissionForm()
    list=[]
    groups=db.session.query(Permission.group).distinct()
 
    for perm in permission:
        obj ={'id':perm.id,'name':perm.name,'group':perm.group,'selected':False}
        for ur in rolePermission:
            if ur.permid==obj['id']:
                obj['selected']=True
                break
        list.append(obj)

    return render_template(
            'rolepermlist.html',
            form=form,
            roles=roles.all(),
            perms=list,
            groups=groups.all()
        )

@blueprint.route('/roleperm/data', methods=['GET'])
@login_required
@admin_required
def role_perm_jsondata():
    id = request.args.get('id', -1, type=int)
    rolePermission=[item.to_dict() for item in PermissionRole.select().filter_by(roleid=id)]
    
    return jsonify(rolePermission)
    #json.dumps(rolePermission)


@blueprint.route('/roleperm/save', methods=['POST'])
@login_required
@admin_required
def role_perm_save():
    form = RolePermissionForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        roleid=form.roleid.data
        permids=form.permids.data
        print(permids)
        PermissionRole.write_data(roleid,permids)
    return json.dumps({'valid':valid,'result':result,'msg':msg })