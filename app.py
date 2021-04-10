from flask import Flask, render_template, request, flash, redirect
from validate_email import validate_email
from data import db_session
from data.users import User
from data.crimes import Crimes

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
        elif request.form['password'] != request.form['password2']:
            flash('Пароли не сходятся', category='error')
        else:
            db_sess = db_session.create_session()
            user = User(
                name=request.form['nickname'],
                email=request.form['email-adress'],
            )
            print(user.name)
            user.set_password(request.form['password'])
            print(user)
            db_sess.add(user)
            db_sess.commit()
            logged = True
            return redirect('/login')

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
    db_sess = db_session.create_session()
    crimes = db_sess.query(User).all()
    print(crimes)
    return render_template('listofcrimes.html', login=logged, crimes=crimes)


@app.route('/crimes/<number>')
def crime(number):
    return render_template('crime.html', number=number, login=logged)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error404.html', login=logged)


if __name__ == '__main__':
    db_session.global_init("db/data.db")
    app.run()
