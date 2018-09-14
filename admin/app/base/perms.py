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

def permission_required(permission):
    print(permission)
    def decorator(f):
        print(permission)
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(permission)
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
 
def admin_required(f): #验证管理员权限的装饰器
    return True # permission_required(Permission.ADMINISTER)(f)
