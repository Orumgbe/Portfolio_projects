from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Register(FlaskForm):
    """Class for registration form"""
    fname = StringField('First name:', validators=[DataRequired(),
                        Length(min=2, max=20)])
    lname = StringField('Last name:', validators=[DataRequired(),
                        Length(min=2, max=20)])
    username = StringField('Username:', validators=[DataRequired(),
                           Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired(),
                            EqualTo('password')])
    signup = SubmitField('sign up')


class Login(FlaskForm):
    """Class for login form"""
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember = BooleanField('Remember me? ')
    login = SubmitField('log in')


class CreatePost(FlaskForm):
    """Class for post creating form"""
    content = TextAreaField("Enter post", validators=[Length(max=150)])
    post = SubmitField('post')
