from flask_login import login_required

from utils.models import User, Post, Comment
from utils import login_manager, app, logout_user, current_user, login_user, db
from utils.oauth import OAuthSignIn
from flask import render_template, redirect, url_for, flash, request, abort
from utils.forms import PostForm, AddCommentForm


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
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


@app.route('/home/view_post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route('/profile/post')
@login_required
def profile():
    posts = Post.query.all()
    users = User.query.all()
    uid = current_user.id
    return render_template('profile.html', posts=posts, users=users, uid=uid)


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
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/profile/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('profile'))


@app.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = AddCommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(url_for("post", post_id=post.id))
    return render_template("view_post_comment.html", title="Comment Post", form=form, post=post)


@app.route('/database')
def database():
    posts = Post.query.all()
    users = User.query.all()
    uid = current_user.id
    comments = Comment.query.all()
    return render_template('database.html', posts=posts, users=users, uid=uid, comments=comments)

# @app.route('/home/search')
# def search():
#     posts = Post.query.whoosh_search(request.args.get('query')).all()
#
#     return render_template('home.html', posts=posts)
