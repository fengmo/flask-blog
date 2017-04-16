# coding: utf-8
from app import app, db, lm
from models import User
from forms import LoginForm, SignUpForm, ChangePasswordForm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', data = "Hello")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname = form.nickname.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash(u'登陆失败，用户名或密码错误，请重新登陆。')
    else:
        flash(u'登陆失败，请重新登陆。')
    return render_template('login.html', form = form)

@app.route('/changepw', methods = ['GET', 'POST'])
@login_required
def changepw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data) and current_user.verify_password(form.new_password.data) is False:
	    current_user.password = form.new_password.data
	    db.session.commit()
	    return redirect(url_for('login'))
	else:
	    flash(u'修改密码失败，原密码不对或新密码与原密码一样')
    else:
	flash(u'修改密码失败，请重新修改')	
    return render_template('changepw.html', form = form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
	user = User.query.filter_by(nickname = form.nickname.data).first()
	if user is None:
	    u = User(nickname = form.nickname.data, password=form.password.data)
	    db.session.add(u)
	    db.session.commit()
	    return redirect(url_for('index'))
	else:
	    flash(u'用户已存在')
    else:
	flash(u'注册失败，请重新注册')
    return render_template('signup.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(403)
def page_not_found(err):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(err):
    return render_template('500.html'), 500
