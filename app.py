from flask import Flask, render_template, request, flash
from validate_email import validate_email
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crimes'
logged = False


@app.route('/')
def main():
    return render_template('main.html', login=logged)


@app.route('/contact')
def contact():
    return render_template('contact.html', login=logged)


@app.route('/registration', methods=['POST', 'GET'])
def reg():
    global logged
    if request.method == 'POST':
        if len(request.form['email-address']) < 7:
            flash('Неверный email', category='error')
        elif not validate_email(request.form['email-address']):
            flash('Несуществующий email', category='error')
        else:
            flash('welcum', category='success')
            logged = True
    return render_template('registration.html', login=logged)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html', login=logged)


@app.route('/profile/<ident>')
def profile(ident):
    return render_template('profile.html', login=logged, id=ident)


@app.route('/map')
def criminalmap():
    return render_template('map.html', login=logged)


@app.route('/add')
def add():
    return render_template('add.html', login=logged)


@app.route('/crimes')
def listofcrimes():
    return render_template('listofcrimes.html', login=logged)


@app.route('/crimes/<number>')
def crime(number):
    return render_template('crime.html', number=number, login=logged)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error404.html', login=logged)


if __name__ == '__main__':
    db_session.global_init("blogs.db")
    app.run()
