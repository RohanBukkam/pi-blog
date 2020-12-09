from utils import UserMixin, app, db, login_manager, ma
from datetime import datetime

class User(UserMixin, db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=True, unique=True)
    email_id = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=True, unique=True)
    profile_picture = db.Column(db.String(500), nullable=False, default='default.jpg')
    post = db.relationship('Post', backref='user', passive_deletes=True)
    comment = db.relationship('Comment', backref='user', passive_deletes=True)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(60), nullable=False, default='General')
    comment = db.relationship('Comment', backref='post', passive_deletes=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sentiment = db.Column(db.Boolean, default=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

#Schemas for the table for flask_marshmallow
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True

# wa.whoosh_index(app, Post)
db.create_all()
