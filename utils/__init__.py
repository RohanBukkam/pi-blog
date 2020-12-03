from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from datetime import timedelta
import os

# App config
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_pyfile('config.cfg')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'

# Session config
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

from utils import routes