# -*- coding: utf-8 -*-


import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'zf(ylx&wc)2018'
PIC_PATH='/Users/YanLixin/Documents/docker/zhexiao/admin/app'
SMS_ACCESS_KEY_ID = "LTAIBQoVVkFipQlB"
SMS_ACCESS_KEY_SECRET = "JLGRCtxDqUezeziqesO0zWa3h6QX92"
SMS_SIGN_NAME = "寻校"
SMS_TEMPLATE_CODE = "SMS_149417802"
