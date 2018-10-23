from app.zx import blueprint
from flask import render_template,request,make_response
from flask_login import login_required
from datatables import DataTable
from app.base.models import User,District,CBD,Grade,Category,School,Show,SchoolGallery,ShowGallery,Province,City,Training,TrainingGallery
from app import db,uploaded_photos,base_path
import sys,os,logging,traceback, json,uuid

from PIL import Image
import flask_excel as excel 
from datetime import  *  

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
        "typeid",
        "typename",
        "desc",
        "sortindex"
    ])
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))

    return json.dumps(table.json())

#begin school
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
    cats=[item.to_dict() for item in Category.list(1)]
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

@blueprint.route('/school/export', methods=['GET'])
@login_required
def school_export():
    # id = request.args.get('id', -1, type=int)
    # result='OK'
    # msg=''
    
    query_sets=[ g for g in  School.query.all()]
   
    column_names =School.get_column_names()

    return excel.make_response_from_query_sets(query_sets, column_names, "xls",200,file_name=u"school.xls",sheet_name='school')
    


@blueprint.route('/school/gallery/list', methods=['GET'])
@login_required
def school_gallery_list():
    schoolid = request.args.get('schoolid', -1, type=int)
    obj = School.query.get(schoolid)
    galleries =[item.to_dict() for item in SchoolGallery.query.filter_by(objid=schoolid)]
    print(len(galleries))
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='school'
        )

@blueprint.route('/school/gallery/create', methods=['GET'])
@login_required
def school_gallery_edit():
    id = request.args.get('schoolid', -1, type=int)
    return render_template(
            'galleryedit.html',
            objid=id,
            type='school'
        )
@blueprint.route('/school/gallery/delete', methods=['POST'])
@login_required
def gallery_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=SchoolGallery.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })


@blueprint.route('/school/gallery/view', methods=['GET'])
@login_required
def school_gallery_photo():
    id = request.args.get('id', -1, type=int)
    gallery = SchoolGallery.query.get(id)
    imagename = os.path.splitext(gallery.path)
    origin = [base_path,r'/files/scools/',str(gallery.objid),r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)

    image_data = open(os.path.join(base_path, originname), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@blueprint.route('/school/gallery/save', methods=['POST'])
@login_required
def school_gallery_save():
    dataX = request.form.get('dataX')
    dataY = request.form.get('dataY')
    dataHeight = request.form.get('dataHeight')
    dataWidth = request.form.get('dataWidth')
   
    gallery = SchoolGallery(**request.form)
    imagename = os.path.splitext(gallery.path)
    fullname = '%s%s%s' % (base_path,r'/files/',gallery.path)
    im = Image.open(fullname)
    id = '-1'
    if gallery.objid is not None:
        id = str(gallery.objid)

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
#end school
#begin show 
@blueprint.route('/show/jsondata', methods=['GET', 'POST'])
@login_required
def show_jsondata():
    table = DataTable(request.args, Show, Show.query, [
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

@blueprint.route('/show/create', methods=['POST'])
@login_required
def show_create():
    school = Show(**request.form)
    result='OK'
    msg=''
    try:
        if int(school.id)>0:
            dd=db.session.query(Show).filter_by(id=school.id)
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

@blueprint.route('/show/edit', methods=['GET'])
@login_required
def show_edit():
    id = request.args.get('id', -1, type=int)
    show = Show.query.get(id)
    if show==None:
        show = Show()
        dt = datetime.now()  
        show.begindate= dt.strftime( '%m-%d-%Y' )  
        show.enddate= dt.strftime( '%m-%d-%Y' )  
        show.price=0
        show.maxprice=0
        print( dt.strftime( '%m-%d-%Y' )   )
    provs=[item.to_dict() for item in Province.query.all()]
    cities=[item.to_dict() for item in City.query.all()]
    districts=[item.to_dict() for item in District.query.all()]
    cbds=[item.to_dict() for item in CBD.query.all()]
    cats=[item.to_dict() for item in Category.list(2)]
    return render_template(
            'showedit.html',
            school=show,
            catList=json.dumps(cats),
            provList=json.dumps(provs),
            cityList=json.dumps(cities),
            districtList=json.dumps(districts),
            cbdList=json.dumps(cbds)
        )

@blueprint.route('/show/delete', methods=['POST'])
@login_required
def show_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=Show.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/show/gallery/list', methods=['GET'])
@login_required
def show_gallery_list():
    id = request.args.get('showid', -1, type=int)
    obj = Show.query.get(id)
    galleries =[item.to_dict() for item in ShowGallery.query.filter_by(objid=id)]
    print(len(galleries))
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='show'
        )

@blueprint.route('/show/gallery/create', methods=['GET'])
@login_required
def show_gallery_edit():
    id = request.args.get('showid', -1, type=int)
    return render_template(
            'galleryedit.html',
            objid=id,
            type='show'
        )
@blueprint.route('/show/gallery/delete', methods=['POST'])
@login_required
def show_gallery_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=ShowGallery.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/show/gallery/view', methods=['GET'])
@login_required
def show_gallery_photo():
    id = request.args.get('id', -1, type=int)
    gallery = ShowGallery.query.get(id)
    imagename = os.path.splitext(gallery.path)
    origin = [base_path,r'/files/shows/',str(gallery.objid),r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)

    image_data = open(os.path.join(base_path, originname), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@blueprint.route('/show/gallery/save', methods=['POST'])
@login_required
def show_gallery_save():
    dataX = request.form.get('dataX')
    dataY = request.form.get('dataY')
    dataHeight = request.form.get('dataHeight')
    dataWidth = request.form.get('dataWidth')
   
    gallery = ShowGallery(**request.form)
    imagename = os.path.splitext(gallery.path)
    fullname = '%s%s%s' % (base_path,r'/files/',gallery.path)
    im = Image.open(fullname)
    id = '-1'
    if gallery.objid is not None:
        id = str(gallery.objid)

    folder =''.join([base_path,r'/files/shows/',id,r'/']) 
    if not os.path.exists(folder):
        os.makedirs(folder)
    origin = [base_path,r'/files/shows/',id,r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)
    im.save(originname)
    cropedIm = im.crop((int(dataX), int(dataY), int(dataWidth), int(dataHeight)))
    imgName=''.join([r'/files/shows/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    originFullName = [base_path,imgName]
    cropedIm.save(''.join(originFullName))
    dataWidth = '190' 
    dataHeight = '130'
    cropedIm = im.resize((int(dataWidth), int(dataHeight)),Image.ANTIALIAS)
    thumName=''.join([r'/files/shows/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumFullName = [base_path,thumName]
    cropedIm.save(''.join(thumFullName))
    result='OK'
    msg=''
    db.session.add(gallery)
    db.session.commit()

    dd=db.session.query(Show).filter_by(id=int(id))
    dd.img=origin
    dd.thumb=origin
    dd.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })
#end show
#begin training 
@blueprint.route('/training/jsondata', methods=['GET', 'POST'])
@login_required
def training_jsondata():
    table = DataTable(request.args, Training, Training.query, [
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

@blueprint.route('/training/create', methods=['POST'])
@login_required
def training_create():
    obj = Training(**request.form)
    result='OK'
    msg=''
    try:
        if int(obj.id)>0:
            dd=db.session.query(Training).filter_by(id=obj.id)
            dd.update(obj.to_dict() )
        else:
            obj.id=None
            db.session.add(obj)
        db.session.commit()
    except Exception as e:  # 这样做就写不了reason了
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.error(repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
        result=None
        msg=str(e)
        #logging.error(e)
        #msg=e

    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/training/edit', methods=['GET'])
@login_required
def training_edit():
    id = request.args.get('id', -1, type=int)
    obj = Training.query.get(id)
    if obj==None:
        obj = Training()
        dt = datetime.now()  
        obj.begindate= dt.strftime( '%m-%d-%Y' )  
        obj.enddate= dt.strftime( '%m-%d-%Y' )  
        obj.price=0
        obj.maxprice=0
        
    provs=[item.to_dict() for item in Province.query.all()]
    cities=[item.to_dict() for item in City.query.all()]
    districts=[item.to_dict() for item in District.query.all()]
    cbds=[item.to_dict() for item in CBD.query.all()]
    cats=[item.to_dict() for item in Category.list(3)]
    return render_template(
            'trainingedit.html',
            obj=obj,
            catList=json.dumps(cats),
            provList=json.dumps(provs),
            cityList=json.dumps(cities),
            districtList=json.dumps(districts),
            cbdList=json.dumps(cbds)
        )

@blueprint.route('/training/delete', methods=['POST'])
@login_required
def training_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=Training.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/training/gallery/list', methods=['GET'])
@login_required
def training_gallery_list():
    id = request.args.get('trainingid', -1, type=int)
    obj = Training.query.get(id)
    galleries =[item.to_dict() for item in TrainingGallery.query.filter_by(objid=id)]
    print(len(galleries))
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='training'
        )

@blueprint.route('/training/gallery/create', methods=['GET'])
@login_required
def training_gallery_edit():
    id = request.args.get('trainingid', type=int)
    return render_template(
            'galleryedit.html',
            objid=id,
            type='training'
        )
@blueprint.route('/training/gallery/delete', methods=['POST'])
@login_required
def training_gallery_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=TrainingGallery.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/training/gallery/view', methods=['GET'])
@login_required
def training_gallery_photo():
    id = request.args.get('id', -1, type=int)
    gallery = TrainingGallery.query.get(id)
    imagename = os.path.splitext(gallery.path)
    origin = [base_path,r'/files/trainings/',str(gallery.objid),r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)

    image_data = open(os.path.join(base_path, originname), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@blueprint.route('/training/gallery/save', methods=['POST'])
@login_required
def training_gallery_save():
    dataX = request.form.get('dataX')
    dataY = request.form.get('dataY')
    dataHeight = request.form.get('dataHeight')
    dataWidth = request.form.get('dataWidth')
   
    gallery = TrainingGallery(**request.form)
    imagename = os.path.splitext(gallery.path)
    fullname = '%s%s%s' % (base_path,r'/files/',gallery.path)
    im = Image.open(fullname)
    id = '-1'
    if gallery.objid is not None:
        id = str(gallery.objid)

    folder =''.join([base_path,r'/files/trainings/',id,r'/']) 
    if not os.path.exists(folder):
        os.makedirs(folder)
    origin = [base_path,r'/files/trainings/',id,r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)
    im.save(originname)
    cropedIm = im.crop((int(dataX), int(dataY), int(dataWidth), int(dataHeight)))
    imgName=''.join([r'/files/trainings/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    originFullName = [base_path,imgName]
    cropedIm.save(''.join(originFullName))
    dataWidth = '190' 
    dataHeight = '130'
    cropedIm = im.resize((int(dataWidth), int(dataHeight)),Image.ANTIALIAS)
    thumName=''.join([r'/files/trainings/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumFullName = [base_path,thumName]
    cropedIm.save(''.join(thumFullName))
    result='OK'
    msg=''
    db.session.add(gallery)
    db.session.commit()

    dd=db.session.query(Training).filter_by(id=int(id))
    dd.img=origin
    dd.thumb=origin
    dd.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })
#end training

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
