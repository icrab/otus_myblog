from flask import Blueprint, render_template, request
from models import User, Session


registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/', methods=('GET', 'POST'), endpoint='index')
def index():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        #request.form.get('')
        args = request.form
        return render_template('registration-success.html', args=args)
