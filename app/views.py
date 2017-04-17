# coding: utf-8
from app import app, db, lm
from models import User, Article, Category, Tag
from forms import LoginForm, SignUpForm, ChangePasswordForm, PostArticleForm, PostCategoryForm, PostTagForm
from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 博客首页
@app.route('/')
def index():
    article_list = Article.query.order_by(Article.ctime.desc())
    article_list.all()
    category_list = Category.query.order_by()
    category_list = category_list.all()
    tag_list = Tag.query.order_by()
    tag_list = tag_list.all()
    return render_template('index.html', article_list=article_list, category_list=category_list, tag_list=tag_list)

# 登录
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect('/')
        flash(u'登陆失败，用户名或密码错误，请重新登陆。')
    return render_template('login.html', form=form)

# 修改密码
@app.route('/changepw', methods = ['GET', 'POST'])
@login_required
def changepw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data) and current_user.verify_password(form.new_password.data) is False:
	    current_user.password = form.new_password.data
	    db.session.commit()
	    return redirect(url_for('login'))
	flash(u'修改密码失败，原密码不对或新密码与原密码一样')
    return render_template('changepw.html', form=form)

# 注册
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
	user = User.query.filter_by(username=form.username.data).first()
	if user is None:
	    u = User(username = form.username.data, password=form.password.data)
	    db.session.add(u)
	    db.session.commit()
	    return redirect(url_for('index'))
	else:
	    flash(u'用户已存在')
    else:
	flash(u'注册失败，请重新注册')
    return render_template('signup.html', form=form)

# 注销
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# 添加文章
@app.route('/post/article', methods = ['GET', 'POST'])
@login_required
def post_article():
    form = PostArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, 
		body=form.body.data, 
		category_id=str(form.category_id.data.id),
		user_id=current_user.id,
		tag_id=str(form.tag_id.data.id))
        db.session.add(article)
	db.session.commit()
        flash(u'文章添加成功')
        return redirect(url_for('index'))
    return render_template('post_article.html', form=form)

# 添加分类
@app.route('/post/category', methods = ['GET', 'POST'])
@login_required
def post_category():
    c_list = Category.query.order_by()
    c_list = c_list.all()
    form = PostCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
	db.session.commit()
        flash(u'分类添加成功')
        return redirect(url_for('index'))
    return render_template('post_category.html', form=form, list=c_list)

# 添加标签
@app.route('/post/tag', methods = ['GET', 'POST'])
@login_required
def post_tag():
    t_list = Tag.query.order_by()
    t_list = t_list.all()
    form = PostTagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
	db.session.commit()
        flash(u'添加成功')
        return redirect(url_for('index'))
    return render_template('post_tag.html', form=form, list=t_list)

# 分类
@app.route('/category/<int:id>')
def category(id):
    category_list = Category.query.order_by()
    if len(category_list.all()) < id:
	return redirect(url_for('index'))
    catgeory_list = category_list.all()
    article_list = Article.query.filter_by(category_id=id)
    article_list = article_list.order_by(Article.ctime.desc())
    article_list = article_list.all()
    tag_list = Tag.query.order_by()
    tag_list = tag_list.all()
    return render_template('category.html', article_list=article_list, category_list=category_list, tag_list=tag_list)

# 标签
@app.route('/tag/<int:id>')
def tag(id):
    tag_list = Tag.query.order_by()
    if len(tag_list.all()) < id:
	return redirect(url_for('index'))
    tag_list = tag_list.all()
    article_list = Article.query.filter_by(tag_id=id).order_by(Article.ctime.desc())
    article_list = article_list.all()
    category_list = Category.query.order_by()
    category_list = category_list.all()
    return render_template('tag.html', article_list=article_list, category_list=category_list, tag_list=tag_list)

# 文章 
@app.route('/article/<int:id>')
def article(id):
    article = Article.query.filter_by(id=id)
    if article.first() is None:
	return redirect(url_for('index'))
    category_list = Category.query.order_by()
    category_list = category_list.all()
    return render_template('article.html', article=article, category_list=category_list)

# 编辑文章
@app.route('/edit/article/<id>', methods = ['GET', 'POST'])
@login_required
def edit_article(id):
    form = PostArticleForm()
    article = Article.query.filter_by(id=id).first()
    if article is not None:
        if form.validate_on_submit():
            article.title=form.title.data
	    article.body=form.body.data
	    article.category_id=str(form.category_id.data.id)
	    article.tag_id=str(form.tag_id.data.id)
	    db.session.commit()
            return redirect(url_for('article', id=article.id))
    else:
	return abort(404)
    form.title.data = article.title
    form.body.data = article.body
    return render_template('edit_article.html', form=form)

# 编辑分类
@app.route('/edit/category/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_category(id):
    form = PostCategoryForm()
    category = Category.query.filter_by(id=id).first()
    if category is not None:
        if form.validate_on_submit():
            category.name=form.name.data
	    db.session.commit()
            return redirect(url_for('index'))
    else:
	return abort(404)
    form.name.data = category.name
    return render_template('edit_category.html', form=form)

# 编辑标签
@app.route('/edit/tag/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_tag(id):
    form = PostTagForm()
    tag = Tag.query.filter_by(id=id).first()
    if tag is not None:
        if form.validate_on_submit():
            tag.name=form.name.data
	    db.session.commit()
            return redirect(url_for('index'))
    else:
	return abort(404)
    form.name.data = tag.name
    return render_template('edit_tag.html', form=form)

# 删除标签
@app.route('/del/tag/<int:id>', methods = ['GET', 'POST'])
@login_required
def del_tag(id):
    form = PostTagForm()
    tag = Tag.query.filter_by(id=id).first()
    if tag is not None:
        if form.validate_on_submit():
	    db.session.delete(tag)
	    db.session.commit()
            return redirect(url_for('index'))
    else:
	return abort(404)
    form.name.data = tag.name
    return render_template('del_tag.html', form=form)

# 删除文章
@app.route('/del/article/<id>', methods = ['GET', 'POST'])
@login_required
def del_article(id):
    form = PostArticleForm()
    article = Article.query.filter_by(id=id).first()
    if article is not None:
        if form.validate_on_submit():
	    db.session.delete(article)
	    db.session.commit()
            return redirect(url_for('index'))
    else:
	return abort(404)
    form.title.data = article.title
    form.body.data = article.body
    form.category_id.data = article.category_id
    form.tag_id.data = article.tag_id
    return render_template('del_article.html', form=form)

# 自定义403页面
@app.errorhandler(403)
def page_not_found(err):
    return render_template('403.html'), 403

# 自定义404页面
@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404

# 自定义500页面
@app.errorhandler(500)
def page_not_found(err):
    return render_template('500.html'), 500
