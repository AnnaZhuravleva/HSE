# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:30:12 2017

@author: Анна
"""
import json
from flask import Flask
from flask import request, render_template

app = Flask(__name__)


def stats_():
    with open('json.txt', 'r', encoding='utf-8') as json_file:
        js = json.load(json_file)
    dict_ = {'Возраст': {}, 'Город': {}, 'Образование': {}, 'Ватрушка': {},
             'Шаньга': {}, 'Расстегай': {}}
    for item in js:
        print(item)
        for key in dict_.keys():
            if key in item.keys() and item[key] not in dict_[key].keys():
                dict_[key][item[key]] = 1
            elif key in item.keys():
                dict_[key][item[key]] += 1
            elif 'Не указано' in dict_[key].keys():
                dict_[key]['Не указано'] += 1
            else:
                dict_[key]['Не указано'] = 1

    return dict_


@app.route('/')
def form():
    return render_template('index.html'), request.args


@app.route('/form/')
def data():
    try:
        with open('json.txt', 'r', encoding='utf-8') as json_file:
            js = json.load(json_file)
            js.append(request.args)
    except Exception:
        js = [request.args]
    with open('json.txt', 'w', encoding='utf-8') as outfile:
        json.dump(js, outfile, ensure_ascii=False)
    stats_()

    return render_template('form.html')


@app.route('/stats/')
def stats():
    return render_template('stats.html', stats=stats_())


@app.route('/json/')
def json1():
    with open('json.txt', 'r', encoding='utf-8') as json_file:
        return render_template('json.html', show=json.load(json_file))


@app.route('/search/')
def search(): return render_template('search.html'), request.args


@app.route('/results/')
def results():
    with open('json.txt', 'r', encoding='utf-8') as json_file:
        js = json.load(json_file)
    result = {}
    for item in js:
        cit = item['Город']
        fil = item[request.args['answer']]
        if cit not in result.keys() and fil != '':
            result[cit] = [fil]
        elif fil != '' and cit in result.keys() and fil not in result[cit]:
            result[cit].append(fil)
    if '' in result.keys():
        result['Город не указан'] = result['']
        del(result[''])

    cakes = {'Ватрушка': "Ватрушку", 'Расстегай' : 'Расстегай', 'Шаньга' : 'Шаньгу'}
    return render_template('results.html', result=result,
                           cake=cakes[request.args['answer']])


if __name__ == '__main__':
    app.run(debug=True)
