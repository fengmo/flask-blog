# coding: utf-8
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(64))
    articles = db.relationship('Article', backref='user')

    def is_authenticated(self):
    	return True

    def is_active(self):
    	return True

    def is_anonymous(self):
    	return False

    def get_id(self):
        return unicode(self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), unique = True)
    body = db.Column(db.Text)
    ctime = db.Column(db.DATETIME, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=0)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), default=0)

    def __repr__(self):
        return '<Article %r>' % (self.title)

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    articles = db.relationship('Article', backref='category')

    def __repr__(self):
        return '<Category %r>' % (self.name)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    articles = db.relationship('Article', backref='tag')

    def __repr__(self):
        return '<Tag %r>' % (self.name)
