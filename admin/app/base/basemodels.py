from flask_login import LoginManager,current_user
from datetime import datetime  
class BaseModel():
    id=0
    status =0
    createdbydate = datetime.now()
    createdbymanagerid = 0
    lastupdatedbydate = datetime.now()
    lastupdatedbymanagerid = 0
    csrf_token=""

    @property
    def status_text( self ):
        print(self.status)
        dict = {0 : "正常", 1 : "已删除", 2 : "已禁用", 3 : "已提交"}
        return dict.get(self.status)

    def mark_del(self):
        self.status=1
        self.lastupdatedbydate=datetime.now()
        self.lastupdatedbymanagerid=current_user.id
        data = {'status': self.status,'lastupdatedbydate':self.lastupdatedbydate,'lastupdatedbymanagerid':self.lastupdatedbymanagerid}
        return data

    def mark_update(self):
        self.lastupdatedbydate=datetime.now()
        self.lastupdatedbymanagerid=current_user.id

    def mark_add(self):
        self.status=0
        self.createdbydate=datetime.now()
        self.createdbymanagerid=current_user.id
        self.lastupdatedbydate=datetime.now()
        self.lastupdatedbymanagerid=current_user.id

