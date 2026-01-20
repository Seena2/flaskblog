from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed   
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flaskblog.models import User
from flask_login import current_user

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    #validation methods to check if username/email already exist 
    def validate_username(self, username):
        # Check if username already exists in the database
        userName=User.query.filter_by(username=username.data).first()
        if userName:  # Placeholder for actual validation logic
            raise ValidationError(f'That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        # Check if email already exists in the database
        userEmail=User.query.filter_by(email=email.data).first()
        if userEmail:  # Placeholder for actual validation logic
            raise ValidationError(f'That email is taken. Please choose a different one.')
        
# Login form, using email and password
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
# Update account form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profilePicture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    #validation methods to check if username/email provided are different from current user's and already exist 
    def validate_username(self, username):
        if username.data != current_user.username:
            userName=User.query.filter_by(username=username.data).first()
            if userName: 
                raise ValidationError(f'That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            userEmail=User.query.filter_by(email=email.data).first()
            if userEmail: 
                raise ValidationError(f'That email is taken. Please choose a different one.')
 
 # Password reset request form
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    # Validate email to check if user with that email exists in the database
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is None: 
            raise ValidationError(f'There is no account with that email. You must register first.')

# Password reset form
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')