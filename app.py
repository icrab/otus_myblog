from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_manager
from posts import post_app
from auth import auth_app
from models import Session, User

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='asdvsadvafnveowinbdfkmb;kn;fldgn;ldskgnbd',
)
app.register_blueprint(post_app, url_prefix='/posts/')
app.register_blueprint(auth_app, url_prefix='/auth/')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Session.query(User).filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('index', unauthorized_redirect=True))


@app.route('/', methods=('GET',), endpoint='index')
def index():
    header = 'Благодатная Жижа'
    links = (
        {'url': url_for('index'), 'name': 'Главная', 'active': False},
    )
    unauthorized_redirected = request.args.get('unauthorized_redirect')

    return render_template('index.html', header=header, links=links, unauthorized_redirect=unauthorized_redirected)


@app.teardown_request
def remove_session(*args):
    Session.remove()


if __name__ == '__main__':
    app.run()
