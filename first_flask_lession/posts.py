from flask import Blueprint, render_template
from models import Tea, User, Comment, Session

post_app = Blueprint('post_app', __name__)


@post_app.route('/', methods=('GET',), endpoint='index')
def index():
    teas = Session.query(Tea).all()
    Session.close()
    return render_template('posts.html', teas=teas)


@post_app.route('/<int:tea_id>/', methods=('GET',), endpoint='single_post')
def single_post(tea_id):
    tea = Session.query(Tea).filter_by(id=tea_id).first()
    comments = Session.query(Comment).filter_by(tea_id=tea_id).all()
    print(comments)
    Session.close()

    return render_template('post.html', id=tea_id, tea=tea, comments=comments)
