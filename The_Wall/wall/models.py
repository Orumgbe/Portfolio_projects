#!/usr/bin/python3
"""This module contains user models for database tables"""

from datetime import datetime
from wall import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """Loads user from user_id stored in a session"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User model table"""
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(45), nullable=True)
    state = db.Column(db.String(45), nullable=True)
    pref_lang = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship("Post", backref="user", lazy=True)

    def __init__(self, **kwargs):
        """Initializes the user"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """Overwrite Object output"""
        return "Account for {} with username {} created on {}"\
               .format(self.fname,
                       self.username,
                       self.created_at)


class Post(db.Model):
    """Post model table"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        """Initializes the post"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """Overwrite Object output"""
        return "Post made by account with user ID {} on {}"\
               .format(self.user_id,
                       self.created_at)
