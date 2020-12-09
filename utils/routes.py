import os
import secrets
from PIL import Image
from utils.forms import RegistrationForm, LoginForm,  UpdateAccountForm
from flask_login import login_required
from utils.models import User, Post, Comment, CommentSchema, UserSchema
from utils import login_manager, app, logout_user, current_user, login_user, db, jsonify, make_response, bcrypt
from utils.oauth import OAuthSignIn
from flask import render_template, redirect, url_for, flash, request, abort
from utils.forms import PostForm, AddCommentForm, RegistrationForm, LoginForm,  UpdateAccountForm
import json


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
    return render_template('home.html', posts=posts, title='Home')


# @app.route('/login')
# def login():
#     next_page = request.args.get('next')
#     return render_template('login.html', next_page=next_page)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email_id=form.email_id.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_id=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/login/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/login/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, name, username, email, profile_picture = oauth.callback()
    if social_id is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))
    # Look if the user already exists
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        # Create the user.
        user = User(social_id=social_id, name=name, username=username, email_id=email, profile_picture=profile_picture)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data
        current_user.email_id = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email_id
    profile_picture = url_for('static', filename='assets/images/' + current_user.profile_picture)
    return render_template('account.html', title='Account', image_file=profile_picture, form=form)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id)
    # comment_schema = CommentSchema(many=True)
    # json_comment_list = comment_schema.dump(comments)
    return render_template('post.html', post=post,
                           comments=comments)  # , json_comment_list=make_response(jsonify({'result': 'success', 'comments': json_comment_list}), 200))


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('postTitle')
        category = request.form.get('postCategory')
        content = request.form.get('editor')
        post = Post(title=title, content=content, user_id=current_user.id, category=category)
        db.session.add(post)
        db.session.commit()
        return render_template('post.html', post=post)
    return render_template('create_post.html', title='New Post', legend='New Post')


@app.route('/profile/post')
@login_required
def profile():
    posts = Post.query.all()
    users = User.query.all()
    return render_template('profile.html', posts=posts, users=users, uid=current_user.id)


@app.route("/profile/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/profile/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        title = request.form.get('postTitle')
        category = request.form.get('postCategory')
        content = request.form.get('editor')
        post = Post.query.filter_by(id=post_id).first()
        post.title = title
        post.category = category
        post.content = content
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    elif request.method == 'GET':
        title = post.title
        post_data = {'title': post.title, 'category': post.category, 'content': post.content}
        return render_template('create_post.html', title='Update Post',
                               post_data=[post.id, post.title, post.category, post.content],
                               legend='Update Post')


@app.route("/profile/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    # Delete its comment first then delete the post
    for comment in post.comment:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('myPosts'))

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def commentSingin():
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('index'))

@app.route("/post/<int:post_id>/addcomment", methods=['GET', 'POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment(content=request.form['commentContent'], post_id=post.id, user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()
    flash("Your comment has been added to the post", "success")

    comments = Comment.query.filter_by(post_id=post_id)
    comment_schema = CommentSchema(many=True)
    json_comment_list = comment_schema.dump(comments)
    json_comment_owner_list = []
    for i in range(len(json_comment_list)):
        json_comment_owner_list.append(
            {'user_id': comments[i].user.id, 'name': comments[i].user.name, 'username': comments[i].user.username,
             'comment_id': comments[i].id})
    return jsonify({'result': 'success', 'comments': json_comment_list, 'owners': json_comment_owner_list})


@app.route("/post/<int:post_id>/getcomment", methods=['GET', 'POST'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id)
    comment_schema = CommentSchema(many=True)
    json_comment_list = comment_schema.dump(comments)
    json_comment_owner_list = []
    for i in range(len(json_comment_list)):
        json_comment_owner_list.append(
            {'user_id': comments[i].user.id, 'name': comments[i].user.name, 'username': comments[i].user.username,
             'comment_id': comments[i].id})
    return jsonify({'result': 'success', 'comments': json_comment_list, 'owners': json_comment_owner_list})


# @app.route('/home/search')
# def search():
#     posts = Post.query.whoosh_search(request.args.get('query')).all()
#
#     return render_template('home.html', posts=posts)

@app.route('/categories')
def categories():
    return render_template('categories.html', title='Categories')


@app.route('/myPosts')
@login_required
def myPosts():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('myPosts.html', posts=posts, title='My posts')

