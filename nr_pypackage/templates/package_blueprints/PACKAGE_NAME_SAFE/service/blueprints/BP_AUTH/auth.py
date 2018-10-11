"""Authentication/Login Blueprint."""
from pprint import pprint

import flask
from flask import Blueprint, flash, render_template, url_for, redirect, request

from flask_login import login_required, login_user, logout_user

from .forms import LoginForm
from .models import LDAPUser

auth_handler = Blueprint(name='auth',
                         import_name=__name__,
                         template_folder='templates',
                         static_folder='static')


@auth_handler.route('/', methods=['GET'])
@login_required
def index():
    """Render auth page."""
    print('>>> auth.index, redirect to landing.index')
    redirect(url_for('landing.index'))


@auth_handler.route('/login', methods=['GET', 'POST'])
def login():
    """Render LoginForm and verify login credentials and if credentials are valid, then login_user."""
    form = LoginForm()

    if form.validate_on_submit():

        username = "" if not form.username.data else form.username.data
        password = "" if not form.password.data else form.password.data

        # Cannot have an empty username or password.
        if not username or not password:
            user = None
        # Validate username and password against LDAP.
        else:
            user = LDAPUser.authenticate_and_init(username, password)

        # Only if a valid user object is returned then login user and redirect.
        if user is not None:
            login_user(user)
            flash('Logged in successfully.')
            print("login successful")
            next_url = request.args.get('next')
            print("next_url: {}".format(next_url))
            return redirect(next_url or url_for('landing.index'))

    print("login first time or unsuccessful")
    return render_template('auth/login.html', form=form)


@auth_handler.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Logout user and redirect to login page."""
    logout_user()
    return redirect(url_for('auth.login'))
