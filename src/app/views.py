from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    catlist = [ # fake array of posts
        {
            'id':'1',
            'name':'幼儿园',
            'schoollist':[{
                'id':1,
                'name':'xxx',
                'desc':'',
                'addr':'',
                'tuition':0,
                'features':'特色',
                'phone':'电话',
                'intro':'特色介绍',
                'team':'团队介绍',
                'founded':'建校时间',
                'city':'',
                'age':'学生年龄段',
                'size':'学校规模',
                'population':'师生数',
                'duration':'上课时间',
                'foreignduration':'外教授课时长',
                'schoolbus':'校车',
                'cramclass':'课后托班'
                }],
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'id':'2',
            'name':'小学',
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        },
        {
            'id':'3',
            'name':'初中',
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        },
        {
            'id':'4',
            'name':'高中',
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        catlist = catlist)


@app.route('/detailed')
def detailed():
    return render_template("detailed.html",
        school = {})


@app.route('/ng')
def ng():
    return render_template("ng.html",
        school = {})

@app.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        flash('login username="' + form.login_username.data + '", login password=' + str(form.login_password.data))
        if form.login_username.data== form.login_password.data:
            return redirect('/index')
        else:
            flash('有户名或密码错误')
    return render_template('login.html',
        title = 'Sign In',
        form = form)

@app.route('/register')
def register():
    return render_template("register.html",
        school = {})
