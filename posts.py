from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import login_required, login_manager
from models import Tea, User, Comment, Session

post_app = Blueprint('post_app', __name__)


@post_app.route('/', methods=('GET',), endpoint='index')
@login_required
def index():
    teas = Session.query(Tea).all()
    links = (
        {'url': url_for('index'), 'name': 'Главная', 'active': False},
        {'name': 'Весь чай', 'active': True}
    )

    return render_template('posts.html', teas=teas, links=links)


@post_app.route('/<int:tea_id>/', methods=('GET',), endpoint='single_post')
@login_required
def single_post(tea_id):
    len_all_teas = len(Session.query(Tea).all())
    Session.close()
    if len_all_teas < tea_id:
        abort(404, description='Tea not found')

    tea = Session.query(Tea).filter_by(id=tea_id).first()
    comments = Session.query(Comment).filter_by(tea_id=tea_id).all()

    links = (
        {'url': url_for('index'), 'name': 'Главная', 'active': False},
        {'url': url_for('post_app.index'), 'name': 'Весь чай', 'active': False},
        {'name': tea.name, 'active': True}
    )

    return render_template('post.html', id=tea_id, tea=tea, comments=comments, links=links)


