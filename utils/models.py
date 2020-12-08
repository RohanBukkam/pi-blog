from datetime import datetime
from utils import UserMixin, app, db, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20))
    #post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.profile_picture}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
db.create_all()


