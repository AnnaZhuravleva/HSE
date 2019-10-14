from SearchSystems import *
from flask import Flask
from flask import request, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html'), request.args


@app.route('/result/')
def result():
    tp = request.args
    if tp['model'] == 2:
        res = model.fasttext.search(tp['sentence'])
    res = [(1, 2, 3), (1, 2, 3)]
    return render_template('result.html', results=res)


if __name__ == '__main__':
    app.run(debug=True)
