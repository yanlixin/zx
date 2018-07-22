from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    loginname = db.Column(db.String(64), index = True, unique = True)
    loginpwd = db.Column(db.String(64), index = True, unique = True)
    nickname = db.Column(db.String(64), index = True, unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(20), index = True, unique = False)
    createdbydate = db.Column(db.String(20), index = True, unique = False)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def check_password(self, password):
        return True #check_password_hash(self.password_hash, password)
    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)