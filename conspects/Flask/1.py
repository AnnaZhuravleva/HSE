from flask import Flask
from flask import request
from flask import render_template
from random import choice
app = Flask(__name__)


@app.route('/')
def index():
    prizes = ['a', 'b', 'c']
    prize = choice(prizes)
    return render_template('main.html', prize=prize)
@app.route('/steal')
def steal():
    number = request.args['number']
    holder = request.args['holder']
    return 'Снимаем деньги с карты {}{}'.format(number,holder)

@app.route('/hi')
def hi():
    if 'name' in request.args and 'surname' in request.ags:
        name = request.ags['name']
        surname = request.ags['surname']
        return '<html><body><strong>Hi {}{}!</strong>></body></html>'.format(name,surname)
    else:
        return'<strong>Скажите</strong>'

if __name__ == '__main__':
    app.run(debug=True)
