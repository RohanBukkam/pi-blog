from utils import UserMixin, app, db, login_manager

class User(UserMixin, db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    email_id = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=True, unique=True)
    profile_picture = db.Column(db.String(500), nullable=False, default='default.jpg')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

db.create_all()