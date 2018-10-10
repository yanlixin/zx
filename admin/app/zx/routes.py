from app.zx import blueprint
from flask import render_template,request,make_response
from flask_login import login_required
from datatables import DataTable
from app.base.models import User,District,CBD,Grade,Category,School,SchoolGallery,Province,City
from app import db,uploaded_photos,base_path
import logging
import json
import sys
import uuid
import os
from PIL import Image

from .forms import SchoolForm,CatForm,CBDForm
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

@blueprint.route('/cbd/jsondata', methods=['GET', 'POST'])
@login_required
def cbd_jsondata():
    table = DataTable(request.args, CBD, CBD.query, [
        "id",
        "name",
        "desc",
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
        if int(school.id)>0:
            dd=db.session.query(School).filter_by(id=school.id)
            dd.update(school.to_dict() )
        else:
            school.id=None
            db.session.add(school)
        db.session.commit()
    except Exception as e:  # 这样做就写不了reason了
        result=None
        msg=str(e)
        logging.error(e)
        #msg=e

    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/school/edit', methods=['GET'])
@login_required
def school_edit():
    id = request.args.get('id', -1, type=int)
    school = School.query.get(id)
    
    provs=[item.to_dict() for item in Province.query.all()]
    cities=[item.to_dict() for item in City.query.all()]
    districts=[item.to_dict() for item in District.query.all()]
    cbds=[item.to_dict() for item in CBD.query.all()]
    grades=[item.to_dict() for item in Grade.query.all()]
    cats=[item.to_dict() for item in Category.query.all()]
    return render_template(
            'schooledit.html',
            school=school,
            catList=json.dumps(cats),
            gradeList=json.dumps(grades),
            provList=json.dumps(provs),
            cityList=json.dumps(cities),
            districtList=json.dumps(districts),
            cbdList=json.dumps(cbds)
        )

@blueprint.route('/school/delete', methods=['POST'])
@login_required
def school_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=School.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


@blueprint.route('/gallery/list', methods=['GET'])
@login_required
def gallery_list():
    schoolid = request.args.get('schoolid', -1, type=int)
    school = School.query.get(schoolid)
    galleries =[item.to_dict() for item in SchoolGallery.query.filter_by(schoolid=schoolid)]
    print(len(galleries))
    return render_template(
            'gallerylist.html',
            school=school,
            galleryList=galleries,
        )

@blueprint.route('/gallery/create', methods=['GET'])
@login_required
def gallery_edit():
    id = request.args.get('schoolid', -1, type=int)
    return render_template(
            'galleryedit.html',
            schoolid=id,
        )


@blueprint.route('/gallery/delete', methods=['POST'])
@login_required
def gallery_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=SchoolGallery.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


@blueprint.route('/gallery/show', methods=['GET'])
@login_required
def gallery_photo():
    id = request.args.get('id', -1, type=int)
    gallery = SchoolGallery.query.get(id)
    imagename = os.path.splitext(gallery.path)
    origin = [base_path,r'/files/scools/',str(gallery.schoolid),r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)

    image_data = open(os.path.join(base_path, originname), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@blueprint.route('/gallery/save', methods=['POST'])
@login_required
def gallery_create():
    dataX = request.form.get('dataX')
    dataY = request.form.get('dataY')
    dataHeight = request.form.get('dataHeight')
    dataWidth = request.form.get('dataWidth')
   
    gallery = SchoolGallery(**request.form)
    imagename = os.path.splitext(gallery.path)
    fullname = '%s%s%s' % (base_path,r'/files/',gallery.path)
    im = Image.open(fullname)
    id = '-1'
    if gallery.schoolid is not None:
        id = str(gallery.schoolid)

    folder =''.join([base_path,r'/files/scools/',id,r'/']) 
    if not os.path.exists(folder):
        os.makedirs(folder)
    origin = [base_path,r'/files/scools/',id,r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)
    im.save(originname)
    cropedIm = im.crop((int(dataX), int(dataY), int(dataWidth), int(dataHeight)))
    imgName=''.join([r'/files/scools/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    originFullName = [base_path,imgName]
    cropedIm.save(''.join(originFullName))
    dataWidth = '190' 
    dataHeight = '130'
    cropedIm = im.resize((int(dataWidth), int(dataHeight)),Image.ANTIALIAS)
    thumName=''.join([r'/files/scools/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumFullName = [base_path,thumName]
    cropedIm.save(''.join(thumFullName))
    result='OK'
    msg=''
    db.session.add(gallery)
    db.session.commit()

    dd=db.session.query(School).filter_by(id=int(id))
    dd.img=origin
    dd.thumb=origin
    dd.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/gallery/upload', methods=['POST'])
def flask_upload():
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
            try:
                fname = '%s%s%s' % ('', uuid.uuid1(), os.path.splitext(file.filename)[1])

                filename = uploaded_photos.save(file, name=fname)
                #print(filename)
                logging.debug('%s url is %s' % (filename, uploaded_photos.url(filename)))
                return json.dumps({'code': 0, 'filename': filename, 'msg': uploaded_photos.url(filename)})
            except Exception as e:
                logging.debug('upload file exception: %s' % e)
                return json.dumps({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return json.dumps({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


@blueprint.route('/category/edit', methods=['GET'])
@login_required
def cat_edit():
    id = request.args.get('id',-1)
    obj = Category.query.get(id)
    if obj==None:
        obj = Category()

    
    form=CatForm(obj=obj)
    return render_template(
            'categoryedit.html',
            form=form,
        )

@blueprint.route('/category/save', methods=['POST'])
@login_required
def cat_save():
    form = CatForm(**request.form)
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = Category()
        form.populate_obj(obj)
        if obj.id=='' or int(obj.id)<=0:
            obj.id=None
            db.session.add(obj)
        else:
            obj.id=obj.id
            o=db.session.query(Category).filter_by(id=obj.id)
            o.update(obj.to_data() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })

@blueprint.route('/category/delete', methods=['POST'])
@login_required
def cat_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=Category.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })



@blueprint.route('/cbd/edit', methods=['GET'])
@login_required
def cbd_edit():
    id = request.args.get('id',-1)
    obj = CBD.query.get(id)
    if obj==None:
        obj = CBD()
    form=CBDForm(obj=obj)
    form.distid.choices = [(-1,'--select--')]
    list=[(str(g.id), g.name) for g in District.query.order_by('sortindex')]
    if list != None and len(list)>0:
        form.distid.choices=form.distid.choices+list

    
    return render_template(
            'cbdedit.html',
            form=form,
        )

@blueprint.route('/cbd/save', methods=['POST'])
@login_required
def cbd_save():
    form = CBDForm(**request.form)
    form.distid.choices = [(-1,'--select--')]
    list=[(str(g.id), g.name) for g in District.query.order_by('sortindex')]
    if list != None and len(list)>0:
        form.distid.choices=form.distid.choices+list
    result='OK'
    valid=True
    msg=''
    if not form.validate_on_submit():
        return json.dumps({'valid':False,'result':result,'msg':form.errors })
    else:
        obj = CBD()
        form.populate_obj(obj)
        if obj.id=='' or int(obj.id)<=0:
            obj.id=None
            db.session.add(obj)
        else:
            obj.id=obj.id
            print(obj.to_data() )
            o=db.session.query(CBD).filter_by(id=obj.id)
            o.update(obj.to_data() )
        db.session.commit()
    return json.dumps({'valid':valid,'result':result,'msg':msg })

@blueprint.route('/cbd/delete', methods=['POST'])
@login_required
def cbd_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=CBD.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })
