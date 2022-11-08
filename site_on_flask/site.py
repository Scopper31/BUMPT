from flask import Flask, render_template, url_for, request
import main


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load')
def load():
    return render_template('load.html')


@app.route('/find')
def find():
    return render_template('find.html')


if __name__ == '__main__':
    app.run(debug=True)
