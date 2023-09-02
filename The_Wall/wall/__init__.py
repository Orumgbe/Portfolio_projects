#!/usr/bin/python3
"""This module contains the routes of the app"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_Secretkey007'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wall.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from wall import routes
