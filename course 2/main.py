# -*- coding: utf-8 -*-
#Веб-сервис: На основе корпуса (новости Школы лингвистики за все время — https://ling.hse.ru/news/) и марковской модели
#сервис генерирует предложения в ответ на реплику пользователя

import urllib.request,re,os,html.parser, csv, html
from random import uniform
from collections import defaultdict
from flask import Flask
from flask import request, render_template

app = Flask(__name__)
def download_page(pageUrl): #Загрузка страницы
    req = urllib.request.Request(pageUrl)
    with urllib.request.urlopen(req) as page:
        html_text = page.read().decode('utf-8', 'ignore')
    return html_text #HTML - текст с тэтагми

def get_news_links(Source_HTML): #Собираем ссылки на новости
    numbers = re.findall('<a href="https://ling.hse.ru/news/(.*?).html"', Source_HTML)
    urls = []
    for number in numbers :
        urls.append('https://ling.hse.ru/news/' + number + '.html')
    return urls

def get_news_text(Source_HTML): #Берем текст новости
    text = re.findall('<div class="lead-in">(.*?)<style type="text/css">', Source_HTML.replace('\n','').replace('\r',''))
    text = tegs_cleaning(''.join(text))
    return text

def tegs_cleaning (html_text): #чистим от тегов и спец символов
    regTag = re.compile('<.*?>', re.DOTALL)  
    regScript = re.compile(u'<script.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)  
    clean = regScript.sub('', html_text)
    clean = regComment.sub("", clean)
    clean = regTag.sub("", clean)
    clean = html.unescape(clean)
    return clean #текст без тэгов

#Генератор текста на основе триграмм
r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')

def gen_lines(corpus):
    data = open(corpus)
    for line in data:
        yield line.lower()

def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model

def generate_sentence(model):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

commonUrl = 'https://ling.hse.ru/news/'
file = open('news.txt', 'w') #открываем файл
for i  in range(1, 40):
    page_url = 'https://ling.hse.ru/news/page' + str(i) + '.html'
    urls = get_news_links(download_page(page_url)) #получаем ссылки на новости
    for url in urls:
        try:
            file.write(get_news_text(download_page(url))) #записываем тексты новостей в файл
        except Exception: #игнорирование ошибок
            pass        
file.close() #закрываем файл
@app.route('/')
def form():    
    return render_template('index.html')
@app.route('/result/')
def data():
   return render_template('result.html', sentence=new_sentence) 
if __name__ == '__main__':
    model = train('news.txt')
    app.run(debug=True)
   
    print(generate_sentence(model))
