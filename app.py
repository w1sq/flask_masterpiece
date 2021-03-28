from flask import Flask, render_template, request, flash , url_for
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crimes'
menu = [
    {'name': 'Главная', 'url': '/'},
    {'name': 'Карта', 'url': 'map'},
    {'name': 'Обратная связь', 'url': 'contact'},
    {'name': "<img src='{url_for('static', filename='img/brawl.png')}>", 'url': 'registration'}
]


@app.route('/')
def main():
    return render_template('main.html', menu=menu)


@app.route('/contact')
def contact():
    return render_template('contact.html', menu=menu)


@app.route('/registration')
def reg():
    return render_template('registration.html', menu=menu)


@app.route('/profile')
def profile():
    return render_template('profile.html', menu=menu)


@app.route('/map')
def map():
    return render_template('map.html', menu=menu)


@app.route('/add')
def add():
    return render_template('add.html', menu=menu)


@app.route('/<number>')
def crime(number):
    return render_template('crime.html', menu=menu)


if __name__ == '__main__':
    app.run()
