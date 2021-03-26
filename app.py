from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lolpog123'
menu = [
    {'name': 'Главная', 'url': 'main'},
    {'name': 'Карта', 'url': 'map'},
    {'name': 'Обратная связь', 'url': 'contact'}
]


@app.route('/')
def index():
    return render_template('welcome.html', menu=menu)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/registration')
def reg():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
