from flask import Blueprint, render_template, request, redirect, url_for, flash
from wateraid import bcrypt, login_manager
from wateraid.database import Database
from wateraid.users.forms import RegistrationForm, LogInForm
from wateraid.users.user import User
from flask_login import login_user, current_user, logout_user
import re

# Login adapted from https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
# Login adapted from https://github.com/boh717/FlaskLogin-and-pymongo/tree/master/app

users_blueprint = Blueprint('users_blueprint', __name__)


@users_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.home'))
    form_register = RegistrationForm()
    if form_register.validate_on_submit():
        # check if user email already exists
        user = Database.reg_users.find_one({'id': re.compile(
            '^' + re.escape(form_register.email.data) + '$', re.IGNORECASE)})
        if user == None:
            # get email address data from form
            email = form_register.email.data
            # encrypt password
            password = bcrypt.generate_password_hash(
                form_register.password.data.encode('utf-8'))
            # insert email and password into database
            Database.reg_users.insert_one({'id': email, 'password': password})
            # Display success message
            flash(
                f'Account created for {form_register.email.data}! You can now log in!', 'success')
            return redirect(url_for('users_blueprint.login'))
        else:
            # Display error message
            flash(
                f'An account for {form_register.email.data} already exists! Please try again with another email address!', 'danger')
    return render_template('register.html', title='Register', form_register=form_register)


@users_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.home'))
    form_signin = LogInForm()
    # for stress testing
    form_check = False
    if request.method == 'POST':
        if request.form.get('test-mode') == 'locust-test':
            form_check = True
        else:
            form_check = form_signin.validate_on_submit()

    if form_check:
        # Find userid in database
        user = Database.reg_users.find_one({'id': re.compile(
            '^' + re.escape(form_signin.email.data) + '$', re.IGNORECASE)})
        # Check if userid and password correct
        if user and bcrypt.check_password_hash(user['password'], form_signin.password.data):
            # create user object
            user_obj = User(user['id'])
            # login user
            login_user(user_obj, remember=form_signin.remember.data)
            # display login success message
            flash("You have logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("main_blueprint.home"))
        else:
            # if user email or password incorrect display error message
            flash('Log in unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form_login=form_signin)


@login_manager.user_loader
def load_user(email):
    """ load user details """
    user_data = Database.reg_users.find_one({"id": email})
    if not user_data:
        return None
    return User(user_data['id'])


@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.home'))
