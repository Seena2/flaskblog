from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# Create the SQLAlchemy db instance
db = SQLAlchemy()

#Create bcrypt instance
bcrypt=Bcrypt()

#Create login manager instance
login_manager=LoginManager()
# login_manager.login_view='login' # specify the login route/view for @login_required
login_manager.login_view='users.login' 
#to style the flash messages on the login page, we set the info class 
login_manager.login_message_category='info'

# intialize the Mail object 
mail=Mail()


# Create function to create the app with configurations, by default use Config class
def create_app(config_class=Config):
    #Instantiate flask application 
    app = Flask(__name__) # :=># set instance of flask to app variable
    # use the config 
    app.config.from_object(Config)
    
    # initialize the extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #To avoid circular imports, import routes at the end
    # import blueprint routes for users and posts
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    # register blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app