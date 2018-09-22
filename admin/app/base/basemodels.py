from flask_login import LoginManager,current_user
from datetime import datetime  
class BaseModel():
    id=0
    status =0
    createddate = datetime.now()
    createdbyuserid = 0
    lasteddate = datetime.now()
    lastedbyuserid = 0
    csrf_token=""

    @property
    def status_text( self ):
        print(self.status)
        dict = {0 : "正常", 1 : "已删除", 2 : "已禁用", 3 : "已提交"}
        return dict.get(self.status)

    def mark_del(self):
        self.status=1
        self.lasteddate=datetime.now()
        self.lastedbyuserid=current_user.id
        data = {'status': self.status,'lasteddate':self.lasteddate,'lastedbyuserid':self.lastedbyuserid}
        return data

    def mark_update(self):
        self.lasteddate=datetime.now()
        self.lastedbyuserid=current_user.id

    def mark_add(self):
        self.status=0
        self.createddate=datetime.now()
        self.createdbyuserid=current_user.id
        self.lasteddate=datetime.now()
        self.lastedbyuserid=current_user.id

