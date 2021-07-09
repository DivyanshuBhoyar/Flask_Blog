from blog.users.uitils import save_picture
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
                                   
# from blog.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route("/RegistrationForm", methods = ['GET', 'POST'])
def registration_page():
      if current_user.is_authenticated:
            return redirect(url_for('main.homepage'))
      form = RegistrationForm()
      if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username = form.username.data, email = form.email.data, password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account Created!', 'success')
            return redirect(url_for('users.login_page'))
      return render_template('register.html', title = 'Registraion', form = form)

@users.route("/LoginForm", methods = ['GET', 'POST'])
def login_page():
      if current_user.is_authenticated:
            return redirect(url_for('main.homepage'))
      form = LoginForm()
      if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                  login_user(user, remember=form.remember.data)
                  next_page = request.args.get('next')
                  return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
            else:
                  flash(f'Login unsuccessful! Please check the email and password.', 'danger')
      return render_template('login.html', title = 'Login', form = form)

@users.route('/logout')
def logout():
      logout_user()
      return redirect(url_for('main.homepage'))

@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
      form = UpdateAccountForm()
      if form.validate_on_submit():
            if form.picture.data:
                  picture_file = save_picture(form.picture.data)
                  current_user.img_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Account Updated!', 'success')
            return redirect(url_for('users.account'))
      elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email

      img_file = url_for('static', filename = 'Profile_Pic/' + current_user.img_file)
      return render_template('account.html', title = 'Account-Page', img_file=img_file, form =form)


@users.route('/user/<string:username>')
def user_posts(username):
      user = User.query.filter_by(username=username).first_or_404()
      posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())
      return render_template('user_posts.html', posts = posts, user=user)