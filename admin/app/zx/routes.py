from app.zx import blueprint
from flask import render_template,request,make_response
from sqlalchemy import or_
from flask_login import login_required
from datatables import DataTable
from app.base.models import User,District,CBD,Grade,Category,School,Show,SchoolGallery,ShowGallery,Province,City,Training,TrainingGallery,TrainingClass,TrainingClassGallery,Lecturer,LecturerGallery
from app import db,uploaded_photos,base_path
from app.config import Config
from urllib import parse
import sys,os,logging,traceback, json,uuid

from PIL import Image
import flask_excel as excel 
from datetime import  *  
import html
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
        "img",
        "addr",
        "features",
        "phone",
        "sortindex"
    ])
    
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))
    table.searchable(lambda qs, sq: qs.filter(or_( School.phone.contains(sq) , School.name.contains(sq),School.addr.contains(sq), School.desc.contains(sq))))

    return json.dumps(table.json())
@blueprint.route('/schoollist', methods=['GET'])
@login_required
def school_list():
    
    pageindex = request.args.get('pageindex',-1)
    orderindex = request.args.get('orderindex','0')
    orderdir = request.args.get('orderdir','asc')
    search = request.args.get('search','')
    return render_template(
            'schoollist.html',
            pageindex=pageindex,
            orderindex=orderindex,
            orderdir=orderdir,
            search=search
        )

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

@blueprint.route('/school/intro/edit', methods=['GET'])
@login_required
def school_intro_edit():
    id = request.args.get('id', -1, type=int)
    pageindex = request.args.get('pageindex')
    orderindex = request.args.get('orderindex')
    orderdir = request.args.get('orderdir')
    search = request.args.get('search')
    gobackurl=''.join(['/zx/schoollist?pageindex=',str(pageindex),'&orderindex=',orderindex,'&orderdir=',orderdir,'&search=',search])

    obj = School.query.get(id)
    if obj.intro==None:
        obj.intro=''
    else:
        obj.intro= html.unescape(obj.intro)
        
    if obj.team==None:
        obj.team=''
    else:
        obj.team= html.unescape(obj.team)
    
        
    return render_template(
            'schoolintro.html',
            obj=obj,
            gobackurl=gobackurl,
        )
@blueprint.route('/school/intro/save', methods=['POST'])
@login_required
def school_intro_save():
    obj = School(**request.form)
    result='OK'
    msg=''
    dd=db.session.query(School).filter_by(id=obj.id)
    dd.update({"intro":obj.intro,"team":obj.team} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

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
    id = request.args.get('schoolid', -1, type=int)
    pageindex = request.args.get('pageindex')
    orderindex = request.args.get('orderindex')
    orderdir = request.args.get('orderdir')
    search = request.args.get('search')
    
    obj = School.query.get(id)
    galleries =[item.to_dict() for item in SchoolGallery.query.filter_by(objid=id)]
    createurl='/zx/school/gallery/create?schoolid='+str(id)
    deleteurl='/zx/school/gallery/delete'
    viewurl='/zx/school/gallery/view'
    defimgurl='/zx/school/gallery/def'
    
    copyurl='/img/school/n/'
    gobackurl=''.join(['/zx/schoollist?pageindex=',str(pageindex),'&orderindex=',orderindex,'&orderdir=',orderdir,'&search=',search])
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='school',
            createurl=createurl,
            deleteurl=deleteurl,
            viewurl=viewurl,
            copyurl=copyurl,
            defimgurl=defimgurl,
            gobackurl=gobackurl

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
    origin = [base_path,r'/files/schools/',str(gallery.objid),r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)

    image_data = open(os.path.join(base_path, originname), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response


@blueprint.route('/school/gallery/def', methods=['POST'])
@login_required
def school_gallery_def():
    result='OK'
    msg=''
    id = request.args.get('id', -1, type=int)
    gallery=SchoolGallery.query.get(id)

    imagename = os.path.splitext(gallery.path)
    path=''.join([base_path,r'/files/schools/',str(gallery.objid),'/'])
    dirs = os.listdir( path )
    dataWidth = '190' 
    dataHeight = '130'
    imgName=''.join([r'/files/schools/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumName=''.join([r'/files/schools/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    #print(''.join([imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]]))
    for file in dirs:
        if len(file)>=36 and len(imagename)>=36 and file[0:36]==imagename[0][0:36]:

            if file ==''.join([imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]]):
                continue
            if file ==''.join([imagename[0],r'_origin_',imagename[1]]):
                continue
            imgName=''.join([r'/files/schools/',str(gallery.objid),r'/',file])
            break
        
    obj=db.session.query(School).filter_by(id=int(gallery.objid))
    obj.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })    

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

    folder =''.join([base_path,r'/files/schools/',id,r'/']) 
    if not os.path.exists(folder):
        os.makedirs(folder)
    origin = [base_path,r'/files/schools/',id,r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)
    im.save(originname)
    cropedIm = im.crop((int(dataX), int(dataY), int(dataWidth), int(dataHeight)))
    imgName=''.join([r'/files/schools/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    originFullName = [base_path,imgName]
    cropedIm.save(''.join(originFullName))
    dataWidth = '190' 
    dataHeight = '130'
    cropedIm = im.resize((int(dataWidth), int(dataHeight)),Image.ANTIALIAS)
    thumName=''.join([r'/files/schools/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
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
@blueprint.route('/showlist', methods=['GET'])
@login_required
def show_list():
    
    pageindex = request.args.get('pageindex',-1)
    orderindex = request.args.get('orderindex','0')
    orderdir = request.args.get('orderdir','asc')
    search = request.args.get('search','')
    return render_template(
            'showlist.html',
            pageindex=pageindex,
            orderindex=orderindex,
            orderdir=orderdir,
            search=search
        )

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
    table.searchable(lambda qs, sq: qs.filter(or_( Show.phone.contains(sq) , School.name.contains(sq),School.addr.contains(sq), School.desc.contains(sq))))

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
@blueprint.route('/show/intro/edit', methods=['GET'])
@login_required
def show_intro_edit():
    id = request.args.get('id', -1, type=int)
    pageindex = request.args.get('pageindex')
    orderindex = request.args.get('orderindex')
    orderdir = request.args.get('orderdir')
    search = request.args.get('search')

    show = Show.query.get(id)
    if show.intro==None:
        show.intro=''
    else:
        show.intro= html.unescape(show.intro)
    
    gobackurl=''.join(['/zx/showlist?pageindex=',str(pageindex),'&orderindex=',orderindex,'&orderdir=',orderdir,'&search=',search])
       
    return render_template(
            'showintro.html',
            show=show,
            gobackurl=gobackurl,
        )
@blueprint.route('/show/intro/save', methods=['POST'])
@login_required
def show_intro_save():
    obj = Show(**request.form)
    result='OK'
    msg=''
    dd=db.session.query(Show).filter_by(id=obj.id)
    dd.update({"intro":obj.intro} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

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
    pageindex = request.args.get('pageindex')
    orderindex = request.args.get('orderindex')
    orderdir = request.args.get('orderdir')
    search = request.args.get('search')

    obj = Show.query.get(id)
    galleries =[item.to_dict() for item in ShowGallery.query.filter_by(objid=id)]
    createurl='/zx/show/gallery/create?showid='+str(id)
    deleteurl='/zx/show/gallery/delete'
    viewurl='/zx/show/gallery/view'
    defimgurl='/zx/show/gallery/def'
    copyurl=Config.IMAGE_DOMAIN+'/img/show/n/'
    gobackurl=''.join(['/zx/showlist?pageindex=',str(pageindex),'&orderindex=',orderindex,'&orderdir=',orderdir,'&search=',search])
 
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='show',
            createurl=createurl,
            deleteurl=deleteurl,
            viewurl=viewurl,
            defimgurl=defimgurl,
            copyurl=copyurl,
            gobackurl=gobackurl
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

@blueprint.route('/show/gallery/def', methods=['POST'])
@login_required
def show_gallery_def():
    result='OK'
    msg=''
    id = request.args.get('id', -1, type=int)
    gallery=ShowGallery.query.get(id)

    imagename = os.path.splitext(gallery.path)
    path=''.join([base_path,r'/files/shows/',str(gallery.objid),'/'])
    dirs = os.listdir( path )
    dataWidth = '190' 
    dataHeight = '130'
    imgName=''.join([r'/files/shows/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumName=''.join([r'/files/shows/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    #print(''.join([imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]]))
    for file in dirs:
        if len(file)>=36 and len(imagename)>=36 and file[0:36]==imagename[0][0:36]:

            if file ==''.join([imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]]):
                continue
            if file ==''.join([imagename[0],r'_origin_',imagename[1]]):
                continue
            imgName=''.join([r'/files/shows/',str(gallery.objid),r'/',file])
            break
        
    obj=db.session.query(Show).filter_by(id=int(gallery.objid))
    obj.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })    

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
    createurl='/zx/training/gallery/create?trainingid='+str(id)
    deleteurl='/zx/training/gallery/delete'
    viewurl='/zx/training/gallery/view'
    defimgurl='/zx/training/gallery/def'
    copyurl='/img/training/n/'  
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='training',
            createurl=createurl,
            deleteurl=deleteurl,
            viewurl=viewurl,
            defimgurl=defimgurl,
            copyurl=copyurl
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
@blueprint.route('/training/gallery/def', methods=['POST'])
@login_required
def training_gallery_def():
    result='OK'
    msg=''
    id = request.args.get('id', -1, type=int)
    gallery=TrainingGallery.query.get(id)
    #print(gallery.path)
    imagename = os.path.splitext(gallery.path)
    path=''.join([base_path,r'/files/trainings/',str(gallery.objid),'/'])
    dirs = os.listdir( path )
    dataWidth = '190' 
    dataHeight = '130'
    imgName=''.join([r'/files/trainings/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumName=''.join([r'/files/trainings/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
   
    for file in dirs:
        
        if len(file)>=36 and len(imagename)>=36 and file[0:36]==imagename[0][0:36]:

            if file ==''.join([imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]]):
                continue
            if file ==''.join([imagename[0],r'_origin_',imagename[1]]):
                continue
            imgName=''.join([r'/files/trainings/',str(gallery.objid),r'/',file])
            break

    obj=db.session.query(Training).filter_by(id=int(gallery.objid))

    obj.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })    
    
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

    if gallery.cat=='2':
        gallery.title= '环境图片' 
    elif gallery.cat=='3':
        gallery.title= '师资团队' 
    elif gallery.cat=='4':
        gallery.title= '课程图片' 
    else:
        gallery.title= '一般图片' 

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
    if gallery.cat==1:
        dd=db.session.query(Training).filter_by(id=int(id))
        dd.img=origin
        dd.thumb=origin
        dd.update({'img':imgName,'thumb':thumName} )
        db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })
#end training




#begin trainingclass 
@blueprint.route('/trainingclass/list', methods=['GET'])
@login_required
def trainingclass_list():
    trainingid = request.args.get('trainingid', -1, type=int)
        
    return render_template(
            'trainingclasslist.html',
            trainingid=trainingid
        )

@blueprint.route('/trainingclass/jsondata', methods=['GET', 'POST'])
@login_required
def trainingclass_jsondata():
    trainingid = request.args.get('trainingid', -1, type=int)
    table = DataTable(request.args, TrainingClass, TrainingClass.query.filter_by(trainingid=trainingid), [
        "id",
        "name",
        "desc",
        "features",
        "sortindex"
    ])
    
    #table.add_data(link=lambda obj: url_for('view_user', id=obj.id))
    #table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))

    return json.dumps(table.json())

@blueprint.route('/trainingclass/create', methods=['POST'])
@login_required
def trainingclass_create():
    obj = TrainingClass(**request.form)
    result='OK'
    msg=''
    try:
        if int(obj.id)>0:
            dd=db.session.query(TrainingClass).filter_by(id=obj.id)
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

@blueprint.route('/trainingclass/edit', methods=['GET'])
@login_required
def trainingclass_edit():
    id = request.args.get('id', -1, type=int)
    trainingid = request.args.get('trainingid', -1, type=int)
    obj = TrainingClass.query.get(id)
    if obj==None:
        obj = TrainingClass()
        obj.trainingid=trainingid
        dt = datetime.now()  
        obj.begindate= dt.strftime( '%m-%d-%Y' )  
        obj.enddate= dt.strftime( '%m-%d-%Y' )  
        obj.price=0
        obj.originalprice=0
        
    return render_template(
            'trainingclassedit.html',
            obj=obj
        )

@blueprint.route('/trainingclass/delete', methods=['POST'])
@login_required
def trainingclass_del():
    id = request.args.get('id', type=int)
    result='OK'
    msg=''
    dd=TrainingClass.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/trainingclass/gallery/list', methods=['GET'])
@login_required
def trainingclass_gallery_list():
    id = request.args.get('classid', -1, type=int)
    obj = TrainingClass.query.get(id)
    galleries =[item.to_dict() for item in TrainingClassGallery.query.filter_by(objid=id)]
    createurl='/zx/trainingclass/gallery/create?classid='+str(id)
    deleteurl='/zx/trainingclass/gallery/delete'
    viewurl='/zx/trainingclass/gallery/view'
    copyurl='/img/trainingclass/n/'
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='trainingclass',
            createurl=createurl,
            deleteurl=deleteurl,
            viewurl=viewurl,
            copyurl=copyurl            
        )

@blueprint.route('/trainingclass/gallery/create', methods=['GET'])
@login_required
def trainingclass_gallery_edit():
    id = request.args.get('classid', type=int)
    return render_template(
            'galleryedit.html',
            objid=id,
            type='trainingclass'
        )
@blueprint.route('/trainingclass/gallery/delete', methods=['POST'])
@login_required
def trainingclass_gallery_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=TrainingClassGallery.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/trainingclass/gallery/view', methods=['GET'])
@login_required
def trainingclass_gallery_photo():
    id = request.args.get('id', -1, type=int)
    gallery = TrainingClassGallery.query.get(id)
    imagename = os.path.splitext(gallery.path)
    origin = [base_path,r'/files/trainingclasses/',str(gallery.objid),r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)

    image_data = open(os.path.join(base_path, originname), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@blueprint.route('/trainingclass/gallery/save', methods=['POST'])
@login_required
def trainingclass_gallery_save():
    dataX = request.form.get('dataX')
    dataY = request.form.get('dataY')
    dataHeight = request.form.get('dataHeight')
    dataWidth = request.form.get('dataWidth')
   
    gallery = TrainingClassGallery(**request.form)
    imagename = os.path.splitext(gallery.path)
    fullname = '%s%s%s' % (base_path,r'/files/',gallery.path)
    im = Image.open(fullname)
    id = '-1'
    if gallery.objid is not None:
        id = str(gallery.objid)

    folder =''.join([base_path,r'/files/trainingclasses/',id,r'/']) 
    if not os.path.exists(folder):
        os.makedirs(folder)
    origin = [base_path,r'/files/trainingclasses/',id,r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)
    im.save(originname)
    cropedIm = im.crop((int(dataX), int(dataY), int(dataWidth), int(dataHeight)))
    imgName=''.join([r'/files/trainingclasses/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    originFullName = [base_path,imgName]
    cropedIm.save(''.join(originFullName))
    dataWidth = '190' 
    dataHeight = '130'
    cropedIm = im.resize((int(dataWidth), int(dataHeight)),Image.ANTIALIAS)
    thumName=''.join([r'/files/trainingclasses/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumFullName = [base_path,thumName]
    cropedIm.save(''.join(thumFullName))
    result='OK'
    msg=''
    db.session.add(gallery)
    db.session.commit()

    dd=db.session.query(TrainingClass).filter_by(id=int(id))
    dd.img=origin
    dd.thumb=origin
    dd.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })
#end trainingclass

#begin lecturer 
@blueprint.route('/lecturer/jsondata', methods=['GET', 'POST'])
@login_required
def lecturer_jsondata():
    table = DataTable(request.args, Lecturer, Lecturer.query, [
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

@blueprint.route('/lecturer/create', methods=['POST'])
@login_required
def lecturer_create():
    obj = Lecturer(**request.form)
    result='OK'
    msg=''
    try:
        if int(obj.id)>0:
            dd=db.session.query(Lecturer).filter_by(id=obj.id)
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

@blueprint.route('/lecturer/edit', methods=['GET'])
@login_required
def lecturer_edit():
    id = request.args.get('id', -1, type=int)
    obj = Lecturer.query.get(id)    
 
    cats=[item.to_dict() for item in Category.list(4)]
    return render_template(
            'lectureredit.html',
            obj=obj,
            catList=json.dumps(cats),
            
        )

@blueprint.route('/lecturer/delete', methods=['POST'])
@login_required
def lecturer_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=Lecturer.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/lecturer/gallery/list', methods=['GET'])
@login_required
def lecturer_gallery_list():
    id = request.args.get('lecturerid', -1, type=int)
    obj = Lecturer.query.get(id)
    galleries =[item.to_dict() for item in LecturerGallery.query.filter_by(objid=id)]
    createurl='/zx/lecturer/gallery/create?lecturerid='+str(id)
    deleteurl='/zx/lecturer/gallery/delete'
    viewurl='/zx/lecturer/gallery/view'
    defimgurl='/zx/lecturer/gallery/def'
    copyurl='/img/lecturer/n/'   
    return render_template(
            'gallerylist.html',
            obj=obj,
            galleryList=galleries,
            type='lecturer',
            createurl=createurl,
            deleteurl=deleteurl,
            viewurl=viewurl,
            defimgurl=defimgurl,
            copyurl=copyurl
        )

@blueprint.route('/lecturer/gallery/create', methods=['GET'])
@login_required
def lecturer_gallery_edit():
    id = request.args.get('lecturerid', type=int)
    return render_template(
            'galleryedit.html',
            objid=id,
            type='lecturer'
        )
@blueprint.route('/lecturer/gallery/delete', methods=['POST'])
@login_required
def lecturer_gallery_del():
    id = request.args.get('id', -1, type=int)
    result='OK'
    msg=''
    dd=LecturerGallery.query.get(id)
    db.session.delete(dd)
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })

@blueprint.route('/lecturer/gallery/view', methods=['GET'])
@login_required
def lecturer_gallery_photo():
    id = request.args.get('id', -1, type=int)
    gallery = LecturerGallery.query.get(id)
    imagename = os.path.splitext(gallery.path)
    origin = [base_path,r'/files/lecturers/',str(gallery.objid),r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)

    image_data = open(os.path.join(base_path, originname), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@blueprint.route('/lecturer/gallery/def', methods=['POST'])
@login_required
def lecturer_gallery_def():
    result='OK'
    msg=''
    id = request.args.get('id', -1, type=int)
    gallery=LecturerGallery.query.get(id)

    imagename = os.path.splitext(gallery.path)
    path=''.join([base_path,r'/files/lecturers/',str(gallery.objid),'/'])
    dirs = os.listdir( path )
    dataWidth = '190' 
    dataHeight = '130'
    imgName=''.join([r'/files/lecturers/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumName=''.join([r'/files/lecturers/',str(gallery.objid),r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    #print(''.join([imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]]))
    for file in dirs:
        if len(file)>=36 and len(imagename)>=36 and file[0:36]==imagename[0][0:36]:

            if file ==''.join([imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]]):
                continue
            if file ==''.join([imagename[0],r'_origin_',imagename[1]]):
                continue
            imgName=''.join([r'/files/lecturers/',str(gallery.objid),r'/',file])
            break
        
    obj=db.session.query(Lecturer).filter_by(id=int(gallery.objid))
    if gallery.cat=='2' :
        obj.update({'avatar':imgName} )
    else:
        obj.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })    

@blueprint.route('/lecturer/gallery/save', methods=['POST'])
@login_required
def lecturer_gallery_save():
    dataX = request.form.get('dataX')
    dataY = request.form.get('dataY')
    dataHeight = request.form.get('dataHeight')
    dataWidth = request.form.get('dataWidth')
   
    gallery = LecturerGallery(**request.form)
    imagename = os.path.splitext(gallery.path)
    fullname = '%s%s%s' % (base_path,r'/files/',gallery.path)
    im = Image.open(fullname)
    id = '-1'
    if gallery.objid is not None:
        id = str(gallery.objid)
    print(gallery.cat)
    gallery.title= '讲师图片' if gallery.cat=='2' else '一般图片'

    folder =''.join([base_path,r'/files/lecturers/',id,r'/']) 
    if not os.path.exists(folder):
        os.makedirs(folder)
    origin = [base_path,r'/files/lecturers/',id,r'/',imagename[0],r'_origin_',imagename[1]]
    originname = ''.join(origin)
    im.save(originname)
    cropedIm = im.crop((int(dataX), int(dataY), int(dataWidth), int(dataHeight)))
    imgName=''.join([r'/files/lecturers/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    originFullName = [base_path,imgName]
    cropedIm.save(''.join(originFullName))
    dataWidth = '190' 
    dataHeight = '130'
    cropedIm = im.resize((int(dataWidth), int(dataHeight)),Image.ANTIALIAS)
    thumName=''.join([r'/files/lecturers/',id,r'/',imagename[0],r'_',dataWidth,r'x',dataHeight,'_',imagename[1]])
    thumFullName = [base_path,thumName]
    cropedIm.save(''.join(thumFullName))
    result='OK'
    msg=''
    db.session.add(gallery)
    db.session.commit()

    dd=db.session.query(Lecturer).filter_by(id=int(id))
    if gallery.cat=='2' :
        dd.update({'avatar':imgName} )
    else:
        dd.update({'img':imgName,'thumb':thumName} )
    db.session.commit()
    return json.dumps({'valid':True,'result':result,'msg':msg })
#end lecturer


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
