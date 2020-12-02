from flask_login import login_required

from utils.models import User
from utils import login_manager, app, logout_user, current_user, login_user, db
from utils.oauth import OAuthSignIn
from flask import render_template, redirect, url_for, flash
from utils.forms import PostForm
from utils.models import Post


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
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
        user = User(social_id=social_id, name=name, username=username, email=email, profile_picture=profile_picture)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))


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
