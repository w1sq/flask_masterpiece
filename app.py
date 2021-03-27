from flask import Flask, render_template, request, flash
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crimes'
menu = [
    {'name': 'Главная', 'url': 'main'},
    {'name': 'Карта', 'url': 'map'},
    {'name': 'Обратная связь', 'url': 'contact'}
]


@app.route('/')
def main():
    return render_template('main.html', menu=menu)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/registration')
def reg():
    return render_template('registration.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/<number>')
def crime(number):
    return render_template('crime.html')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run()
