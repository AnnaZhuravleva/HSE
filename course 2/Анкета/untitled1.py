# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:30:12 2017

@author: Анна
"""
import re, json
from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route('/')
def form():    
    return render_template('index.html'), request.args

@app.route('/form/')
def data():
    with open ('form.txt', mode='a', encoding = 'utf-8') as f:
         for key in request.args:
            f.write(key)
            f.write('--')
            f.write(request.args[key])
            f.write(' ')
         f.write('Sent. \n')
         
    return render_template('form.html')
     
@app.route('/stats/')

def stats():
    with open (r'form.txt','r', encoding = 'utf-8') as f:        
        vatrushka = {}
        shanga = {}
        rasstegay = {}
        edu = {}
        city = {}
        for line in f.read().split(' '):
            line.capitalize()
            v = re.search('vatrushka--(.*)',line)
            s = re.search('shanga--(.*)',line)
            r = re.search('rasstegay--(.*)',line)
            e = re.search('answer--(.*)',line)
            c = re.search('city--(.*)',line)
            if v:
                if v.group(1) not in vatrushka:
                    vatrushka[v.group(1)] = 1
                else:
                    vatrushka[v.group(1)] += 1
            if s:                
                if s.group(1) not in shanga:
                    shanga[s.group(1)] = 1
                else:
                    shanga[s.group(1)] += 1
            if r:
                if r.group(1) not in rasstegay:
                    rasstegay[r.group(1)] = 1
                else:
                    rasstegay[r.group(1)] += 1
            if c:
                if c.group(1) not in rasstegay:
                    city[c.group(1)] = 1
                else:
                    city[c.group(1)] += 1        
            if 'школьник' in line or 'выпускник' in line  or 'студент' in line or 'высшее' in line:
                if line not in edu:
                    edu[e.group(1)] = 1
                else:
                    edu[e.group(1)] += 1
        with open ('stats.txt', mode='w', encoding = 'utf-8') as f:
            f.write('Ватрушка\n')
            for i in vatrushka:
                f.write(i)
                f.write(' ')
                f.write(str(vatrushka[i]))
                f.write('\n')
            f.write('\n\n\n')
            f.write('Шаньга\n')
            for i in shanga:
                f.write(i)
                f.write(' ')
                f.write(str(shanga[i]))
                f.write('\n')
            f.write('\n\n\n')
            f.write('Расстегай\n')
            for i in rasstegay:
                f.write(i)
                f.write(' ')
                f.write(str(rasstegay[i]))
                f.write('\n')
            f.write('\n')
            f.write('\n\n\n')
            f.write('Город\n')
            for i in city:
                f.write(i)
                f.write(' ')
                f.write(str(city[i]))
                f.write('\n')
            f.write('\n')
            f.write('\n\n\n')
            f.write('Уровень образования\n')
            for i in edu:
                f.write(i)
                f.write(' ')
                f.write(str(edu[i]))
                f.write('\n')
            f.write('\n')
            f.write('\n\n\n')
    with open ('stats.txt', mode='r', encoding = 'utf-8') as f:
        stats = f.readlines()
        
    return render_template('stats.html', stats = stats)  

@app.route('/json/')
def json1():
    with open ('form.txt', mode='r', encoding = 'utf-8') as f:
        with open('jsondata.json', mode='r+', encoding = 'utf-8') as k:
            mass = f.read().split(' ')
            for i in mass:
                json.dump(i, k, ensure_ascii = False)
                k.write(' ')
            show = k.readlines()

            return render_template('forjson.html', show = show)    
@app.route('/search/')
def search():    
    return render_template('search.html'), request.args    

@app.route ('/results/')  
def results():
    with open (r'form.txt','r', encoding = 'utf-8') as f: 
        lines = f.read()
        answers = lines.split('Sent. ')
        cities = {}
        cake = request.args
        for key in request. args:
            if 'vatrushka' in request.args[key]:
                for line in answers:
                    v = re.search('vatrushka--(.*)',line)
                    c = re.search('city--(.*)',line)
                    if c.group(1) not in cities:
                        cities[c.group(1)] = v.group(1)
                    else:
                        if cities[c.group(1)] != v.group(1):
                           cities[c.group(1)] = cities[c.group(1)] + ', ' + v.group(1)
                        else:
                            continue
        for key in request. args:
            if 'shanga' in request.args[key]:
                for line in answers:
                    s = re.search('shanga--(.*)',line)
                    c = re.search('city--(.*)',line)
                    if c.group(1) not in cities:
                        cities[c.group(1)] = s.group(1)
                    else:
                        if cities[c.group(1)] != s.group(1):
                           cities[c.group(1)] = cities[c.group(1)] + ', ' + s.group(1)
                        else:
                            continue
        for key in request. args:
            if 'rasstegay' in request.args[key]:
                for line in answers:
                    r = re.search('rasstegay--(.*)',line)
                    c = re.search('city--(.*)',line)
                    if c.group(1) not in cities:
                        cities[c.group(1)] = r.group(1)
                    else:
                        if cities[c.group(1)] != r.group(1):
                           cities[c.group(1)] = cities[c.group(1)] + ', ' + r.group(1)
                        else:
                            continue
        return render_template('results.html', cities = cities,cake = cake )
                     
 
if __name__ == '__main__':
    app.run(debug=True)
