from app.pm import blueprint
import sys,os,logging, json,uuid
from sqlalchemy import and_,or_
from flask import render_template,request,make_response,jsonify
from flask_login import login_required,current_user
from wtforms.validators import ValidationError
from datatables import DataTable
from datetime import datetime 


from app import db,uploaded_photos,base_path
from .models import UUID_DEF,Doc,loimport
from .forms import DocForm

@blueprint.route('/doc/list', methods=['GET'])
@login_required
def doc_list():
    projid = request.args.get('projectid', UUID_DEF)
    return render_template('doc/doclist.html',projid=projid)

@blueprint.route('/doc/data', methods=['GET', 'POST'])
@login_required
def doc_jsondata():
    table = DataTable(request.args, Doc, Doc.query, [
        "id",
        "no",
        "title",
        "alias",
        "desc",
        "filetype",
        "lastedversion",
        "status_text"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))
    table.searchable(lambda qs, sq: qs.filter(or_(doc.no.contains(sq) , doc.name.contains(sq), doc.desc.contains(sq))))
    return json.dumps(table.json(),)
    #return jsonify(table)

@blueprint.route('/doc/new', methods=['GET'])
@login_required
def doc_new():
    projid = request.args.get('projectid')
    obj = Doc(id=UUID_DEF)
    form=DocForm(obj=obj)
    return render_template(
            'doc/docnew.html',
            form=form,
            projid=projid
        )

@blueprint.route('/doc/edit', methods=['GET'])
@login_required
def doc_edit():
    id = request.args.get('id', UUID_DEF)
    obj = doc.query.get(id)
    if obj==None:
        obj = doc(id=UUID_DEF)
    form=docForm(obj=obj)
    return render_template(
            'doc/docedit.html',
            form=form,
        )

@blueprint.route('/file/post', methods=['POST'])
def flask_upload():
    projid = request.args.get('projectid')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            logging.debug('No file part')
            return json.dumps({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            logging.debug('No selected file')
            return json.dumps({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            fname = '%s%s%s' % ('', uuid.uuid1(), os.path.splitext(file.filename)[1])
            doc=Doc()
            doc.title=file.filename
            doc.projid=projid
            doc.preview=file.read()
            doc.mark_add()
            db.session.add(doc)
            db.session.commit()
            return json.dumps({'code': 0, 'filename': '', 'msg': ''})
    else:
        return json.dumps({'code': -1, 'filename': '', 'msg': 'Method not allowed'})



@blueprint.route('/doc/view', methods=['GET'])
@login_required
def doc_view():
    id = request.args.get('id', UUID_DEF)
    obj = Doc.query.get(id)
    if obj==None:
        obj = Doc(id=UUID_DEF)
    form={"name":obj.name,"desc":obj.desc}
    return render_template(
            'doc/docview.html',
            proj=form,
        )

@blueprint.route('/doc/save', methods=['POST'])
@login_required
def doc_save():
    form = DocForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Doc()
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
            o=db.session.query(Doc).filter_by(id=obj.id)
            o.update(obj.to_dict() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })


