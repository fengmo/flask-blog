# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class LoginForm(FlaskForm):
    nickname = StringField(u'用户', validators=[DataRequired(), Length(5, 15)])
    password = PasswordField(u'密码', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    nickname = StringField(u'用户', validators=[DataRequired(), Length(5, 15), Regexp('[A-Za-z][A-Za-z0-9]*$')])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(8, 20)])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[DataRequired()])
    new_password = PasswordField(u'新密码', validators=[DataRequired(), Length(8, 20)])
