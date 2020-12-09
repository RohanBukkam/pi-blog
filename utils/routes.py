import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from utils.models import User
from utils.forms import RegistrationForm, LoginForm,  UpdateAccountForm
from utils import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from utils.oauth import OAuthSignIn



posts = [
    {
        'author': 'Simran Kaur',
        'title': 'Blog One',
        'content': 'First Blog Content',
        'date posted': 'December 1, 2020'
    },
    {
        'author': 'Akansha Sharma',
        'title': 'Blog Two',
        'content': 'Second Blog Content',
        'date_posted': 'December 2, 2020'
    }

]

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


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
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


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
    return render_template('account.html', title='Account',
                           image_file=profile_picture, form=form)
