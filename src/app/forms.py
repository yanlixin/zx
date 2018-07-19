from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login_username = StringField('login_username', validators=[DataRequired()])
    login_password = StringField('login_password', validators=[DataRequired()])