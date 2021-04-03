from flask import Flask, render_template, request, flash, url_for
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crimes'


@app.route('/')
def main():
    return render_template('main.html', login=False)


@app.route('/contact')
def contact():
    return render_template('contact.html', login=True)


@app.route('/registration')
def reg():
    return render_template('registration.html', login=True)


@app.route('/login')
def login():
    return render_template('login.html', login=True)


@app.route('/profile')
def profile():
    return render_template('profile.html', login=True)


@app.route('/map')
def criminalmap():
    return render_template('map.html', login=True)


@app.route('/add')
def add():
    return render_template('add.html', login=True)


@app.route('/crimes')
def listofcrimes():
    return render_template('listofcrimes.html', login=True)


@app.route('/crimes/<number>')
def crime(number):
    return render_template('crime.html', number=number, login=True)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error404.html', login=True)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run()
