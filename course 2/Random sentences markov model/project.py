# -*- coding: utf-8 -*-
# Веб-сервис: На основе корпуса (новости Школы лингвистики за все время — https://ling.hse.ru/news/)
# и марковской модели сервис генерирует предложения в ответ на реплику пользователя

from flask import Flask
from flask import request, render_template
from markovmodel import *
# from buildcorpus import *   ## заново собирает корпус

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html'), request.args


@app.route('/result/')
def result():
    tmp = generate_sentence(model)
    while True:
        if len(tmp.split(' ')) >= 3:
            break
        tmp = generate_sentence(model)
    return render_template('result.html', sentence=tmp)


if __name__ == '__main__':
    model = train('corpus/news.txt')
    #  model = train('tolstoy.txt') - генирирует предложения на основе корпуса Л.Н. Толстого
    app.run(debug=True)
