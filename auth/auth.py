from logging import getLogger
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from models import Session, User
from werkzeug.exceptions import BadRequest

auth_app = Blueprint('auth_app', __name__)

logger = getLogger(__name__)


def validate_registration_data(username, password, email):
    if not(
        username
        and len(username) >= 3
        and password
        and len(password) >= 8
        and email
    ):
        raise BadRequest('Username has to be at least 3 symbols and password at least 8, email not null')


def get_registration_data():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    return username, password, email


def validate_username_and_email_unique(username, email):
    if Session.query(User).filter_by(name=username).count():
        raise BadRequest('Username already exists')
    if Session.query(User).filter_by(mail=email).count():
        raise BadRequest('Username with this email already exists')


@auth_app.route('/register/', methods=('GET', 'POST'), endpoint='register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth_app.index'))

    if request.method == 'GET':
        return render_template('auth/register.html')

    username, password, email = get_registration_data()
    validate_registration_data(username, password, email)
    validate_username_and_email_unique(username, email)
    user = User(username, password, email)
    Session.add(user)
    try:
        Session.commit()
    except Exception:
        logger.exception('Failed to add user')
        Session.rollback()

    login_user(user)
    return redirect(url_for('index'))


@auth_app.route('/login/', methods=('GET', 'POST'), endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_app.index'))

    if request.method == 'GET':
        return render_template('auth/login.html')

    username, password, email = get_registration_data()

    user = Session.query(User).filter_by(name=username).one_or_none()
    if not user:
        raise BadRequest('Username invalid')
    if not user.password == User.hash_password(password):
        raise BadRequest('Password invalid')

    login_user(user)
    return redirect(url_for('index'))


@auth_app.route('/logout/', methods=('GET',), endpoint='logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



