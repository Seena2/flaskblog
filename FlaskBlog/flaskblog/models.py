from datetime import datetime
from flaskblog import db,login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import os # For secret key
from datetime import datetime
from flask import current_app as app

# Load user for login manager
@login_manager.user_loader  
def load_user(user_id):
    return User.query.get(int(user_id))

#DB Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # method to generate reset token
    def get_reset_token(self, expires_sec=1800):
        # Generates a time-limited token for password reset
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
         # The dumps() method serializes the data (user id) and signs it with a timestamp
        token = serializer.dumps(self.id, salt='password-reset-salt')
        return token
            

    # verify reset token method
    @staticmethod #(class method to be called without an instance,"self" as parameter instead takes "token")
    def verify_reset_token(token, expires_sec=1800):
        # Validates the token and returns the user if valid, otherwise None.
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            # loads() method verifies the signature and checks the timestamp
            # max_age sets the expiration time for the token
            user_id = s.loads(token,salt='password-reset-salt', max_age=expires_sec)['user_id']
        except:
            return None # Token is invalid or expired
        # If valid, find the user in the database return user
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"    
