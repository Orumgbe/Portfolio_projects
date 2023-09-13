#!/usr/bin/python3
"""This module contains the web app routes"""

from flask import render_template, url_for, redirect, request
from wall import app, bcrypt, db
from wall.forms import Register, Login, CreatePost, UpdateProfile
from wall.models import User, Post
from flask_login import current_user, login_user, login_required, logout_user


@app.route('/', strict_slashes=False)
@app.route('/index/', strict_slashes=False)
def index():
    """This renders the landing page"""
    return render_template("landing.html")


@app.route('/home/', strict_slashes=False)
def home():
    """This renders the home page"""
    return render_template("home.html")


@app.route('/register/', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """This renders the sign up page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    register = Register()
    if register.validate_on_submit():
        hashpwd = bcrypt.generate_password_hash(register.password.data)\
                  .decode('utf-8')
        user = User(fname=register.fname.data, lname=register.lname.data,
                    username=register.username.data, email=register.email.data,
                    password=hashpwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=register)


@app.route('/login/', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """This renders the log in page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login = Login()
    if login.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=login.email.data).first()
        db.session.close()
        form_pwd = login.password.data
        if user is not None:
            if bcrypt.check_password_hash(user.password, form_pwd):
                login_user(user, remember=login.remember.data)
                page = request.args.get('next')
                if page:
                    return redirect(page)
                return redirect(url_for('home'))
    return render_template("login.html", form=login)


@app.route('/logout/', strict_slashes=False)
def logout():
    """This logs out user"""
    logout_user()
    return render_template("landing.html", form=login)


@app.route('/profile/', strict_slashes=False)
@app.route('/profile/<username>', strict_slashes=False)
@login_required
def profile(username=None):
    """This renders the profile page"""
    if username:
        with app.app_context():
            user = User.query.filter_by(username=username).first()
        db.session.close()

        if user:
            return render_template("profile.html", user=user)
        else:
            return "This user does not exist"
    else:
        return render_template("profile.html", user=current_user)


@app.route('/profile/update', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def updateprofile():
    """This renders the update profile page"""
    form = UpdateProfile()
    if form.validate_on_submit():
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.username = form.username.data 
        current_user.bio = form.bio.data 
        current_user.email = form.email.data 
        current_user.country = form.country.data 
        current_user.state = form.state.data 
        current_user.pref_lang = form.pref_lang.data 
        db.session.commit()
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.username.data = current_user.username
        form.bio.data = current_user.bio
        form.email.data = current_user.email
        form.country.data = current_user.country
        form.state.data = current_user.state
        form.pref_lang.data = current_user.pref_lang
    return render_template("updateprofile.html", user=current_user,
                           form=form)


@app.route('/profile/delete/<int:user_id>', methods=['POST'], strict_slashes=False)
@login_required
def deleteprofile(user_id=0):
    """This deletes and returns to landing page"""
    if user_id > 0:
        with app.app_context():
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
    return redirect(url_for('index'))


@app.route('/the_wall/', strict_slashes=False)
def wall():
    """This renders the wall page"""
    with app.app_context():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.options(db.joinedload(Post.user)).paginate(page=page, per_page=9)
    db.session.close()

    idx = ["one", "two", "three", "four", "five", "six",
           "seven", "eight", "nine"]
    while len(posts.items) < 9:
        posts.items.append("Write on the wall")
    zip_posts = zip(posts, idx)
    return render_template("wall.html", posts=zip_posts, pager=posts)


@app.route('/the_wall/new', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def newpost():
    """This renders page to accept new post input"""
    block = CreatePost()
    if block.validate_on_submit():
        post = Post(content=block.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('wall'))
    return render_template("post.html", form=block)


@app.route('/the_wall/<post_id>/delete', methods=['GET', 'POST'], strict_slashes=False)
def deletePost(post_id):
    """This deletes post and redirects to wall"""
    with app.app_context():
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('wall'))


@app.route('/chat/', strict_slashes=False)
def chat():
    """This renders the chat page"""
    return render_template("chat.html")


@app.route('/about/', strict_slashes=False)
def about():
    """This renders the about page"""
    return render_template("about.html")


@app.route('/contact_us/', strict_slashes=False)
def contact():
    """This renders the contacts page"""
    return render_template("contact.html")
