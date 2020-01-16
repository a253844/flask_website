from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, ValidationError , TextAreaField 
from wtforms.fields.html5 import EmailField
from app_blog.author.model import UserReister
from wtforms import BooleanField

class FormRegister(FlaskForm):

    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(5, 30)
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    password2 = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Register New Account')

    def validate_email(self, field):
        if UserReister.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register by somebody')

    def validate_username(self, field):
        if UserReister.query.filter_by(username=field.data).first():
            raise ValidationError('UserName already register by somebody')

class FormLogin(FlaskForm):

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('PassWord', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('Keep Logged in')

    submit = SubmitField('Log in')

class ChangeInfo(FlaskForm):

    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(5, 30)
    ])

    submit = SubmitField('Change Your Infomation')
