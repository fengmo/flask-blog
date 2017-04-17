# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import Category, Tag

class LoginForm(FlaskForm):
    username = StringField(u'用户', validators=[DataRequired(), Length(5, 15)])
    password = PasswordField(u'密码', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    username = StringField(u'用户', validators=[DataRequired(), Length(5, 15), Regexp('[A-Za-z][A-Za-z0-9]*$')])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(8, 20)])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[DataRequired()])
    new_password = PasswordField(u'新密码', validators=[DataRequired(), Length(8, 20)])

class PostArticleForm(FlaskForm):
    title = StringField(u'标题', validators=[DataRequired(), Length(3, 64)])
    body = TextAreaField(u'内容')
    category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(), get_pk=lambda v: str(v.id), get_label=lambda v: v.name)
    tag_id = QuerySelectField(u'分类', query_factory=lambda: Tag.query.all(), get_pk=lambda v: str(v.id), get_label=lambda v: v.name)

class PostCategoryForm(FlaskForm):
    name = StringField(u'分类名', validators=[DataRequired(), Length(3, 64)])

class PostTagForm(FlaskForm):
    name = StringField(u'标签', validators=[DataRequired(), Length(3, 64)])
