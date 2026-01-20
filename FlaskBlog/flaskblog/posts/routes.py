from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog.posts.forms import CreatePostForm    
from flaskblog.models import Post
from flaskblog import db
from flask_login import current_user, login_required    

# Create a Blueprint instance for posts package
posts = Blueprint('posts', __name__)

#Dummy blog posts
# posts=[
#     {
#         'author':'Kenna Barreddu',
#         'title':'Blog post one',
#         'content':'First post content',
#         'date_posted':'April 18,2020'
#     },
#     {
#         'author':'Jane Doe',
#         'title':'Blog post two',
#         'content':'second post content',
#         'date_posted':'May 4,2021'
#     }
# ]



#Create new blogpost route
@posts.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    # create instance of CreatePostForm
    form = CreatePostForm()
    # validate and process the form on submit
    if form.validate_on_submit():
        # Create new Post instance and add to db
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title="New Post", form=form, legend="Create new post")

# View a blog post route
@posts.route("/post/<int:post_id>")
def post(post_id):
    # fetch the post by id if exist or return 404 if not found
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

#Update post
@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def updatePost(post_id):
    # fetch the post by id if exist or return 404 if not found
    post = Post.query.get_or_404(post_id)
    # check if the current user is the author of the post, if not abort with 403 error
    if post.author != current_user:
        abort(403) #HTTP forbidden error
    # if the user and author is the same
    # create instance of CreatePostForm
    form = CreatePostForm() 
    # Validate the for on submit and commit update to the DB
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data     
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    # else if the request method is GET, populate the form fields with existing post data
    elif request.method=='GET':
    # send post data to populate the form field with post data, so that user can view and update at same time
        form.title.data=post.title
        form.content.data=post.content     
    return render_template('create_post.html', title="Update post", form=form, legend="Update post")

#Delete post
@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def deletePost(post_id):
    # fetch the post by id if exist or return 404 if not found
    post = Post.query.get_or_404(post_id)
    # check if the current user is the author of the post, if not abort with 403 error
    if post.author != current_user:
        abort(403) #HTTP forbidden error
    # delete the post from db
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

