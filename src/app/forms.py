from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login_username = StringField('login_username', validators=[DataRequired()])
    login_password = StringField('login_password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    register_mobile = StringField('register_mobile', validators=[DataRequired()])
    register_password = PasswordField('register_password', validators=[DataRequired()])
    sms_code = StringField('sms_code', validators=[DataRequired()])
   

    def validate_username(self, register_mobile):
        user = User.query.filter_by(loginname=register_mobile.data).first()
        if user is not None:
            raise ValidationError('Please use a different register mobile.')
