from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', endpoint='index')
def index():
    return 'Hello index!'


if __name__ == '__main__':
    app.run(debug=True)