import random
from flask import Flask
from flask import request, render_template
import pymorphy2

app = Flask(__name__)
pmm = pymorphy2.MorphAnalyzer()
punct = '[.,!«»?&@"$\[\]\(\):;%#&\'—-*]'
dict_ = {}
normdict_ = {}
restricted = ['masc', 'femn', 'anim', 'neut', 'perf', 'impf', 'ms-f']

def builddict():
    with open('words.txt', 'r', encoding='utf-8') as f:
        words = ' '.join(f.read().split('\n'))
        words = words.split(' ')
        new_words = [word.strip(punct).lower() for word in words]
        for word in new_words:
            p = pmm.parse(word)
            for i in range(len(p)):
                try:
                    if p[i].tag not in dict_.keys():
                        dict_[p[i].tag] = [word]
                    else:
                        if word not in dict_[p[i].tag]:
                            dict_[p[i].tag].append(word)
                except UnicodeEncodeError:
                    pass
                try:
                    if p[i].tag.POS not in normdict_.keys():
                        normdict_[p[i].tag.POS] = [p[i].normal_form]
                    else:
                        if p[i].normal_form not in normdict_[p[i].tag.POS]:
                            normdict_[p[i].tag.POS].append(p[i].normal_form)
                except UnicodeEncodeError:
                    pass
        return


@app.route('/')
def form():    
    return render_template('index.html'), request.args


def repl():
    text = request.args['sentence']
    reply = []
    text = text.split(' ')
    puncts = {}
    for number, word in enumerate(text):
        if word[-1] in punct:
            puncts[number] = word[-1]
        word = word.strip(punct)
        p = pmm.parse(word)[0].tag
        if p in dict_.keys():
            kk = random.choice(list(range(len(dict_[p]))))
            reply.append(dict_[p][kk])
        else:
            tmp = random.choice(list(range(len(normdict_[p.POS]))))
            ss = ','.join(str(p).strip('()').split(' ')).split(',')
            ss = {w for w in ss if w not in restricted}
            while tmp < len(normdict_[p.POS]):
                try:
                    reply.append(pmm.parse(normdict_[p.POS][tmp])[0].inflect(ss).word)
                    break
                except:
                    tmp += 1
            if tmp == len(normdict_[p.POS]):
                reply.append(word)
    reply[0] = reply[0].title()
    for i in range(len(reply)):
        if i in puncts.keys():
            reply[i] += puncts[i]
    return ' '.join(reply)


@app.route('/result/')
def result():
    new_sentence = repl()
    return render_template('result.html', sentence=new_sentence)


if __name__ == '__main__':
    builddict()
    app.run(debug=True)
