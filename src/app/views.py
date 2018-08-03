from flask import render_template, flash, redirect, session, url_for, request, g ,jsonify, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
import json
from sqlalchemy import or_
#from flask_babel import _
from app import app, db, lm
from .forms import LoginForm,RegistrationForm
from .models import User,School,Grade,Category,District

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    gradelist=[item.to_dict() for item in Grade.query.all()]
    return render_template("index.html",
        title = 'Home',
        gradelist =gradelist)

@app.route('/detailed')
def detailed():
    id = request.args.get('id', 1, type=int)
    data = School.query.get(id)
    #jsonify(User.query.get_or_404(id).to_dict())
    return render_template("detailed.html",
        school = data)


@app.route('/ng')
def ng():
    id = request.args.get('id', -1, type=int)
    catid = request.args.get('catid', -1, type=int)
    data=[item.to_dict() for item in School.query.filter(or_(School.gradeid==id,-1==id)).filter(or_(School.catid==catid,-1==catid))]
    distList=[item.to_dict() for item in District.query.all()]
    return render_template("ng.html",
        id=id,
        distlist=distList,
        schoollist = data)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    print(form.login_username.data)
    if form.validate_on_submit():
        session['remember_me'] = False
        
    if form.validate_on_submit():
        user = User.query.filter_by(loginname=form.login_username.data).first()
        if user is None or not user.check_password(form.login_password.data):
            flash('账号或密码错误')
            return redirect(url_for('login'))
        login_user(user, False)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/checkloginname')
def checkloginname():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(loginname=form.register_mobile.data).first()
        if user :
            flash('登录名已存,请重新确认后输入!')
        else :
            user = User(loginname=form.register_mobile.data)
            user.set_password(form.register_password.data)
            db.session.add(user)
            db.session.commit()
            flash('恭喜您, 你已经注册成功了!')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register',
                           form=form)

@app.route('/admin')
def admin():
    return render_template("admin.html",
        school = {})

@app.route('/users', methods=['GET'])
def admin_shcoollist():
    page = request.args.get('offset', 0, type=int)
    per_page = min(request.args.get('limit', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)