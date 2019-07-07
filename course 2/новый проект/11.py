from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
import urllib.request
import re
import html

app = Flask(__name__)
regTag = re.compile('<.*?>', re.DOTALL)
vowels = ['А','Е','И','У','О','Ё','Э','Ю','Ы', 'Я', 'а','е','и','у','о','ё','э','ю','ы', 'я']


reg_word_trnsltn = re.compile('<td class="uu">.*?</td><td class="uu">.*?</td><td></td><td class="uu">.*?</td>', flags = re.DOTALL)
dictat = {}

def list_of_urls_for_letters(base_url_for_letter_page):
    urls = []
    for letter in ['c', 'd']:
        for number in range(10):
            url = base_url_for_letter_page+letter+str(number)
            urls.append(url)
        for add_letter in ['a', 'b', 'c', 'd', 'e', 'f']:
            url = base_url_for_letter_page+letter+add_letter
            urls.append(url)
    return urls

def create_html(url, encoding):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'  
    req = urllib.request.Request(url, headers={'User-Agent':user_agent})  
    with urllib.request.urlopen(req) as response:
        html = response.read().decode(encoding)
    return html

def create_dictat(url):
    text = create_html(url, 'windows-1251')
    found = reg_word_trnsltn.findall(text)
    cleaned = []
    for item in found:
        word = re.sub('<td></td>',', ',item)
        clean = re.sub('(<.*?>)|(&nbsp;)|\'', '', word)
        with_yat = re.sub('&#1123;', 'ѣ', clean)
        with_i = re.sub('&#1110;', 'i', with_yat)
        with_f = re.sub('&#1139;', 'ѳ', with_i)
        two_first = re.sub(r'<td class="uu"><a name="e1\w\d"></a><font color="#808080">ба</font>&nbsp;</td>', '', with_f)
        dict_item = two_first.split(' ')
        cleaned.append(dict_item)
        dictat [dict_item[0].strip(',')] = dict_item[1].strip(',')
    return dictat

urls = list_of_urls_for_letters('http://www.dorev.ru/ru-index.html?l=')
for url in urls:
    create_dictat(url)
    
def dorevate(word):
    prefix = [ 'бес', 'чрес', 'черес']
    for pref in prefix:
        if word.startswith(pref):
            word = word.replace(pref, pref[0:len(pref)-1]+'з')
    if word[-1]!='и':
        if vowels.count(word[word.find('и')+1])!=0:
            word = word.replace('и', 'i')
    if vowels.count(word[-1])==0 and word[-1]!='ь' and word[-1]!='ъ':
        word = word+'ъ'
    return word

@app.route('/dorev/')
def index():
    description = weather_in_scopje ('<div class="now__desc"><span class="tip _top _center">.*?</span></div>')
    temperature = weather_in_scopje ('<span class="nowvalue__text_l"><span class="nowvalue__sign">.*?</span>.*?<span class="nowvalue__text_m">.</span></span>')
    return render_template ('form.html', description = description, temperature = temperature)

@app.route('/word/')
def word():
    word = request.args['s']
    if list(dictat.keys()).count(word)!=0:
        trsltn = dictat[word]
    else:
        trsltn = dorevate(word)
    return trsltn

def weather_in_scopje(regex):
    html = create_html ('https://www.gismeteo.ru/weather-skopje-3253/now/', 'utf-8')
    reg_weather = re.compile(regex, flags= re.DOTALL)
    weather_html = reg_weather.findall(html)
    weather = regTag.sub("", weather_html[0])
    return weather
                               
@app.route('/dorev/news')
def news():
    html = create_html ('https://www.sports.ru/', 'utf-8')
    regcyril = re.compile('[А-Яа-я]+', re.DOTALL)
    words = re.findall(regcyril, html)
    dorevwords = []
    number = 0
    maximum = []
    for word in words:
        if list(dictat.keys()).count(word)!=0:
            trsltn = dictat[word]
        else:
            trsltn = dorevate(word)
        dorevwords.append(trsltn)
        if dorevwords.count(trsltn)>number:
            number = dorevwords.count(trsltn)
            if maximum.count(trsltn) != 1:
                maximum.append(trsltn)
    return 'Самые частотные слова:'+str(maximum[0:11])+'\n'+str(dorevwords)

@app.route('/dorev/test')
def test():
    variants = {'ans0':{'Лень':'Лѣнь'}, 'ans1': {'Век':'Вѣк'}, 'ans2':{'Дева':'Дѣва'}, 'ans3':{'Бѣжѣвый':'Бежевый'}, 'ans4':{'Пѣна':'Пена'}, 'ans5':{'Зенитъ':'Зѣнитъ'}, 'ans6':{'Плѣсень':'Плѣсѣнь'}, 'ans7':{'Алексѣй':'Алексей'}, 'ans8':{'Еда':'ѣда'}, 'ans9':{'Сѣмья':'Семья'}}
    return render_template('test.html', variants = variants)

@app.route('/dorev/test/results/')
def test_results():
    results = test_results()
    return 'Ваш балл: '+str(results['points'])+' из 10. Вы ошиблись в вопросах:'+str(results['false'])

def test_results():
    points = 0
    false = []
    for i in range(0,10):
        if request.args['ans'+str(i)]=='r':
            points += 1
        else:
            false.append(i)
    results = {}
    results['points']=points
    results['false']=false
    return results
               
if __name__ == '__main__':
    app.run(debug=True)


