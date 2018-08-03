from app.zx import blueprint
from flask import render_template,request
from flask_login import login_required
from datatables import DataTable
from app.base.models import User,District,Grade,Category,School,Province,City
from app import db
import logging
import json
import sys

from .forms import SchoolForm
@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')


@blueprint.route('/manager/jsondata', methods=['GET', 'POST'])
@login_required
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

@blueprint.route('/district/jsondata', methods=['GET', 'POST'])
@login_required
def district_jsondata():
    table = DataTable(request.args, District, District.query, [
        "id",
        "name",
        "sortindex"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))

    return json.dumps(table.json())

@blueprint.route('/category/jsondata', methods=['GET', 'POST'])
@login_required
def category_jsondata():
    table = DataTable(request.args, Category, Category.query, [
        "id",
        "name",
        "desc",
        "sortindex"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))

    return json.dumps(table.json())


@blueprint.route('/school/jsondata', methods=['GET', 'POST'])
@login_required
def school_jsondata():
    table = DataTable(request.args, School, School.query, [
        "id",
        "name",
        "desc",
        "addr",
        "features",
        "phone",
        "sortindex"
    ])
    
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))

    return json.dumps(table.json())

@blueprint.route('/school/create', methods=['POST'])
@login_required
def school_create():
    school = School(**request.form)
    result='OK'
    msg=''
    try:
        if int(school.id)>=0:
            dd=db.session.query(School).filter_by(id=school.id)
            logging.debug(dd)
            dd.update(school.to_dict() )
        else:
            db.session.add(school)
        db.session.commit()
    except Exception as e:  # 这样做就写不了reason了
        result=None
        msg=str(e)
        logging.error(e)
        #msg=e

    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/schooledit', methods=['GET'])
@login_required
def school_edit():
    id = request.args.get('id', 1, type=int)
    school = School.query.get(id)
    
    provs=[item.to_dict() for item in Province.query.all()]
    cities=[item.to_dict() for item in City.query.all()]
    districts=[item.to_dict() for item in District.query.all()]
    grades=[item.to_dict() for item in Grade.query.all()]
    cats=[item.to_dict() for item in Category.query.all()]
    return render_template(
            'schooledit.html',
            school=school,
            catList=json.dumps(cats),
            gradeList=json.dumps(grades),
            provList=json.dumps(provs),
            cityList=json.dumps(cities),
            districtList=json.dumps(districts)
        )