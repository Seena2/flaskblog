from flaskblog import  db
from flaskblog.models import User, Post
from flask import current_app as app

#use context manager to create the database
with app.app_context():
    db.create_all()
    print("Database created!")
        