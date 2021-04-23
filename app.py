from flask import Flask, render_template, request, flash, redirect, abort
from validate_email import validate_email
from data import db_session
from data.users import User
from data.crimes import Crimes
from werkzeug.security import generate_password_hash
import lob

app = Flask(__name__)
app.config["SECRET_KEY"] = "crimes"
logged = False
user_data = None


@app.route("/")
def main():
    return render_template("main.html", login=logged)


@app.route("/contact")
def contact():
    return render_template("contact.html", login=logged)


@app.route("/registration", methods=["POST", "GET"])
def reg():
    global logged
    if request.method == "POST":
        if len(request.form["email-address"]) < 7:
            flash("Неверный email", category="error")
        elif not validate_email(request.form["email-address"]):
            flash("Несуществующий email", category="error")
        elif request.form["password"] != request.form["password2"]:
            flash("Пароли не сходятся", category="error")
        else:
            db_sess = db_session.create_session()
            user = User(
                name=request.form["nickname1"],
                email=request.form["email-address"],
            )
            user.set_password(request.form["password"])
            db_sess.add(user)
            db_sess.commit()
            return redirect("/login")

    return render_template("registration.html", login=logged)


@app.route("/login", methods=["POST", "GET"])
def login():
    global logged
    global user_data
    if request.method == "POST":
        db_sess = db_session.create_session()
        email = request.form["email-address"]
        password = request.form["password"]
        dbuser_inf = db_sess.query(User).filter(User.email == email).first()
        if dbuser_inf and dbuser_inf.check_password(password):
            logged = True
            user_data = dbuser_inf
            return redirect("/")
        else:
            flash("Неправильно введена почта или пароль", category="error")
    return render_template("login.html", login=logged)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    global logged
    db_sess = db_session.create_session()
    name = user_data.name
    if request.method == "POST":
        logged = False
        return redirect("/")
    return render_template("profile.html", login=logged, name=name)


@app.route("/map")
def criminalmap():
    return render_template("map.html", login=logged)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        db_sess = db_session.create_session()
        kind = request.form["kindofcrime"]
        short = request.form["crimetitle"]
        adress = request.form["adress"]
        details = request.form["aboutcrime"]
        crime = Crimes(kind=kind, title=short, content=details, adress=adress)
        db_sess.add(crime)
        db_sess.commit()
        return redirect("/crimes")
    return render_template("add.html", login=logged)


@app.route("/crimes")
def listofcrimes():
    db_sess = db_session.create_session()
    crimes = db_sess.query(Crimes).all()
    return render_template("listofcrimes.html", login=logged, crimes=crimes)


@app.route("/crimes/<number>")
def crime(number):
    db_sess = db_session.create_session()
    crime = db_sess.query(Crimes).filter(Crimes.id == number).first()
    if crime:
        return render_template("crime.html", crime=crime, login=logged)
    else:
        return pageNotFound(404)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("error404.html", login=logged)


if __name__ == "__main__":
    db_session.global_init("db/data.db")
    app.run()
