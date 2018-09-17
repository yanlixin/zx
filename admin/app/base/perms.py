#from app import db, login_manager
#from flask_login import UserMixin
#from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
#from datetime import datetime

from flask_login import LoginManager,current_user
from app import db
from functools import wraps
from flask import abort

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
from datetime import datetime  

class Permission:
    FOLLOW = 0x01 #关注其他用户
    COMMENT = 0x02 #评论
    WHITE_ARTICLES = 0x04 #写文章
    MODERATE_COMMENTS = 0x08 #管理评论
    ADMINISTER = '46395cd8-b9ae-11e8-81c9-6c40088e9afc' #管理员权限

def permission_required(permission):
    print()
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(permission)
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
 
def admin_required(f): #验证管理员权限的装饰器
    return permission_required(Permission.ADMINISTER)(f)
