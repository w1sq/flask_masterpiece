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
admins = ["artem.kokorev2005@yandex.ru"]


@app.route("/")
def main():
    return render_template("main.html", login=logged, user_data=user_data)


@app.route("/contact")
def contact():
    return render_template("contact.html", login=logged, user_data=user_data)


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

    return render_template("registration.html", login=logged, user_data=user_data)


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
    return render_template("login.html", login=logged, user_data=user_data)


@app.route("/profile/<id>", methods=["POST", "GET"])
def profile(id):
    global logged
    global user_data
    db_sess = db_session.create_session()
    lich_crimes = db_sess.query(Crimes).filter(Crimes.user_id == id).all()
    if request.method == "POST":
        logged = False
        user_data = None
        return redirect("/")
    if user_data.id != id:
        user_data1 = db_sess.query(User).filter(User.id == id).first()
        return render_template(
            "profile.html",
            login=logged,
            user_data=user_data1,
            crimes=lich_crimes,
            admin=False,
        )
    elif str(user_data.email) in admins:
        return render_template(
            "profile.html",
            login=logged,
            user_data=user_data,
            crimes=lich_crimes,
            admin=True,
        )
    else:
        return render_template(
            "profile.html",
            login=logged,
            user_data=user_data,
            crimes=lich_crimes,
            admin=False,
        )


@app.route("/admin")
def admin():
    if str(user_data.email) in admins:
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).all()
        return render_template(
            "admin.html", login=logged, user_data=user_data, questions=questions
        )
    else:
        abort(404)


@app.route("/map")
def criminalmap():
    return render_template("map.html", login=logged, user_data=user_data)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        db_sess = db_session.create_session()
        kind = request.form["kindofcrime"]
        short = request.form["crimetitle"]
        adress = request.form["adress"]
        details = request.form["aboutcrime"]
        if user_data:
            crime = Crimes(
                kind=kind,
                title=short,
                content=details,
                adress=adress,
                user_id=user_data.id,
            )
        db_sess.add(crime)
        db_sess.commit()
        return redirect("/crimes")
    return render_template("add.html", login=logged, user_data=user_data)


@app.route("/crimes")
def listofcrimes():
    db_sess = db_session.create_session()
    crimes = db_sess.query(Crimes).all()
    return render_template(
        "listofcrimes.html", login=logged, crimes=crimes, user_data=user_data
    )


@app.route("/crimes/<number>")
def crime(number):
    db_sess = db_session.create_session()
    crime = db_sess.query(Crimes).filter(Crimes.id == number).first()
    if crime:
        return render_template(
            "crime.html", crime=crime, login=logged, user_data=user_data
        )
    else:
        return pageNotFound(404)


@app.route("/delete_news/<number>")
def delete(number):
    db_sess = db_session.create_session()
    crime = db_sess.query(Crimes).filter(Crimes.id == number).first()
    if crime:
        db_sess.delete(crime)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/crimes")


@app.route("/edit_news/<number>", methods=["POST", "GET"])
def edit(number):
    db_sess = db_session.create_session()
    crime = db_sess.query(Crimes).filter(Crimes.id == number).first()
    if request.method == "POST":
        kind = request.form["kindofcrime"]
        short = request.form["crimetitle"]
        adress = request.form["adress"]
        details = request.form["aboutcrime"]
        if user_data:
            crime1 = Crimes(
                kind=kind,
                title=short,
                content=details,
                adress=adress,
                user_id=user_data.id,
                created_date=crime.created_date,
            )
        db_sess.delete(crime)
        db_sess.merge(crime1)
        db_sess.commit()
        return redirect("/crimes")
    if crime:
        return render_template(
            "edit.html", crime=crime, login=logged, user_data=user_data
        )
    else:
        return pageNotFound(404)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("error404.html", login=logged, user_data=user_data)


if __name__ == "__main__":
    db_session.global_init("db/data.db")
    app.run()
