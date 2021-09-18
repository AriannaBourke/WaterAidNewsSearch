from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wateraid.database import Database
import re

# Login adapted from https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
# Login adapted from https://github.com/boh717/FlaskLogin-and-pymongo/tree/master/app


class RegistrationForm(FlaskForm):
    """ Registration form class
        Fields include email, password and password confirmation
        With form validation where fields cannot be empty, 
        email must be in correct format and passwords must match"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Your Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Database.reg_users.find_one(
            {'email': re.compile('^' + re.escape(email.data) + '$', re.IGNORECASE)})
        if user:
            raise ValidationError(
                'This email has already been taken. Please try a different one!')


class LogInForm(FlaskForm):
    """ Login form class
        Fields include email and password
        With form validation where fields cannot be empty and 
        email must be in correct format"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
