import os
class Config:
    #set secret key for forms
    # app.config['SECRET_KEY'] = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6-SEENA'
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    # SQLite database configuration
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    # email server constants
    # MAIL_SERVER='smtp.googlemail.com'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587 
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('EMAILSERVER_US') 
    MAIL_PASSWORD=os.environ.get('EMAILSERVER_PASS') 
    # 'MAIL_DEBUG=True