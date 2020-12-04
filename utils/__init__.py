from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from datetime import timedelta
import os

# App config
app = Flask(__name__, template_folder='../templates', static_folder='../static')
#app.config.from_pyfile('config.cfg')

# Google Cloud SQL (change this accordingly)
PASSWORD = os.environ.get('PASSWORD')
PUBLIC_IP_ADDRESS = os.environ.get('PUBLIC_IP_ADDRESS')
DBNAME = os.environ.get('DBNAME')
PROJECT_ID = os.environ.get('PROJECT_ID')
INSTANCE_NAME = os.environ.get('INSTANCE_NAME')

app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config['GOOGLE_LOGIN_CLIENT_ID'] = os.environ.get('GOOGLE_LOGIN_CLIENT_ID')
app.config['GOOGLE_LOGIN_CLIENT_SECRET'] = os.environ.get('GOOGLE_LOGIN_CLIENT_SECRET')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'

# Session config
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

from utils import routes