from flask import Flask, request, render_template
from posts import post_app
from registration import registration_app
from models import Session, Tea, User, Comment

app = Flask(__name__)
app.register_blueprint(post_app, url_prefix='/posts/')
app.register_blueprint(registration_app, url_prefix='/registration/')


@app.route('/', methods=('GET', 'POST'), endpoint='index')
def index():
    header = 'Благодатная Жижа'
    if request.method == 'POST':
        return '<h1>Hello index post!</h1>'

    return render_template('index.html', header=header)


@app.teardown_request
def remove_session(*args):
    Session.close()


if __name__ == '__main__':
    app.run(debug=True)