from flask import render_template, request, Blueprint
from blog.models import Post
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def homepage():
      posts = Post.query.order_by(Post.date_posted.desc())
      return render_template('home.html', posts = posts)

@main.route("/blog_about")
def about_page():
    return render_template('blog_about.html', title = 'About')