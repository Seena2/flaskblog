from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm,ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.models import User, Post
from flaskblog import db, bcrypt
from flaskblog.users.utils import save_picture, sendResetEmail

# Create a Blueprint for users
users = Blueprint('users', __name__)

#Registration Route
@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #Create instance of RegistrationForm
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash the password before storing it to db, and decode to utf-8 string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create user instance
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Add user to db session
        db.session.add(user)
        # Commit user to db
        db.session.commit()
        # return f"Account created for {form.username.data}!"
        flash(f'Your account has been created, you are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    #pass the form instance to the template
    return render_template('register.html', title="Register", form=form)

#Login Route
@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mainhome'))
    form = LoginForm()
    if form.validate_on_submit():
        # # use dummy data to simulate login
        # if form.email.data=="admin@blog.com" and form.password.data=="Admin123":
        #     flash(f'Login successful for {form.email.data}!', 'success')
        #     return redirect(url_for('main.home'))

        # Query DB if user exists and verify password user provided via the form against hashed password in DB
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #if the user exists and password is correct, log them in using login_user function
            login_user(user, remember=form.remember.data)
            #get the next parameter from url if exists to redirect to the page user wanted to access before login 
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))          
        else:
            flash(f'Login failed. Please check your credentials.', 'danger')
    return render_template('login.html', title="Login", form=form)

#Logout Route
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home')) 



#restricted route only accessible to logged in users
#Account Route
@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    # Create instance of UpdateAccountForm and pass to template
    form = UpdateAccountForm()
    # validate and process the update account form submission
    if form.validate_on_submit():
        # check if a new profile picture has been uploaded
        if form.profilePicture.data:
            #save the picture and get the filename
            picture_file = save_picture(form.profilePicture.data)
            #update current_user's image_file attribute
            current_user.image_file = picture_file
        # change current_user's username and email to the newly provided form data and commit to db
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        #populate the form fields with current_user data
        form.username.data=current_user.username
        form.email.data=current_user.email
    profileImageFile=url_for('static', filename='profilePics/' + current_user.image_file)
    return render_template('account.html', title="Account", profileImageFile=profileImageFile, form=form)

#user Route : posts created by a user
@users.route("/user/<string:username>")
def user_posts(username):
    # get the user by username or return 404 if not found
    user = User.query.filter_by(username=username).first_or_404()
    page=request.args.get('page',1,type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts,user=user)

# password reset request route
@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    # make sure user is logged out
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # create form object for reset request 
    form = RequestResetForm()
    if form.validate_on_submit:
        # get the user using its email 
        user=User.query.filter_by(email=form.email.data).first()
        # if the user exists, send reset email containing the reset token link
        if user:
            sendResetEmail(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)

#password reseting route
@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  
    #verify the token and get the user
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        # hash the new password before storing it to db, and decode to utf-8 string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # update user's password
        user.password=hashed_password
        db.session.commit()
        # send notification to user, "success" is bootstrap class used for styling
        flash(f'Your password has been updated, you are now able to log in!', 'success')        
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title="Reset Password", form=form)
    