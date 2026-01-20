from flask import Blueprint, render_template, request
from flaskblog.models import Post

# Create a Blueprint instance for main package
main = Blueprint('main', __name__)

#Home/root Route
@main.route("/")
@main.route("/home")
def home():
    # create posts by querying the Post model
    # posts = Post.query.all()
    # use pagination to limit number of posts per page
    # get the page number from the url parameter, default to 1 if not present
    page=request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

#About Route
@main.route("/about")
def about():
    return render_template('about.html', title="About")