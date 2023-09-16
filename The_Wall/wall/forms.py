from flask_wtf import FlaskForm
from flask_login import current_user
from wall import app, db
from wall.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class Register(FlaskForm):
    """Class for registration form"""
    fname = StringField('First name:', validators=[DataRequired(),
                        Length(min=2, max=25)])
    lname = StringField('Last name:', validators=[DataRequired(),
                        Length(min=2, max=25)])
    username = StringField('Username:', validators=[DataRequired(),
                           Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired(),
                            EqualTo('password')])
    signup = SubmitField('sign up')

    def validate_username(self, username):
        """Ensures username is unique"""
        with app.app_context():
            user = User.query.filter_by(username=username.data).first()
        db.session.close()
        if user:
            raise ValidationError("Username already taken")

    def validate_email(self, email):
        """Ensures email is unique"""
        with app.app_context():
            user = User.query.filter_by(email=email.data).first()
        db.session.close()
        if user:
            raise ValidationError("Email already taken")


class Login(FlaskForm):
    """Class for login form"""
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember = BooleanField('Remember me? ')
    login = SubmitField('log in')


class CreatePost(FlaskForm):
    """Class for post creating form"""
    content = TextAreaField("Enter post", validators=[DataRequired(), Length(max=150)], render_kw={'rows': 5, 'cols': 50})
    post = SubmitField('post')


class UpdateProfile(FlaskForm):
    """Class for profile update form"""
    fname = StringField('First name:', validators=[DataRequired(),
                        Length(min=2, max=25)])
    lname = StringField('Last name:', validators=[DataRequired(),
                        Length(min=2, max=25)])
    username = StringField('Username:', validators=[DataRequired(),
                           Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    bio = TextAreaField('Bio:')
    country = StringField('Country:', validators=[Length(max=45)])
    state = StringField('State:', validators=[Length(max=45)])
    pref_lang = StringField('Preferred language:', validators=[Length(max=20)])

    update = SubmitField('save changes')

    def validate_username(self, username):
        """Ensures username is unique"""
        if username.data != current_user.username:
            with app.app_context():
                user = User.query.filter_by(username=username.data).first()
            db.session.close()
            if user:
                raise ValidationError("Username already taken")

    def validate_email(self, email):
        """Ensures email is unique"""
        if email.data != current_user.email:
            with app.app_context():
                user = User.query.filter_by(email=email.data).first()
            db.session.close()
            if user:
                raise ValidationError("Email already taken")
