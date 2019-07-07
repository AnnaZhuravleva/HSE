import re, json
from flask import Flask
from flask import request, render_template
from pymystem3 import Mystem
import pymorphy2
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
m = Mystem()

app = Flask(__name__)

@app.route('/')
def form():    
    return render_template('index.html'), request.args

@app.route('/result/')
def data():
    text = request.args['sentence']
    text = text.split(' ')
    punct = '[.,!«»?&@"$\[\]\(\):;%#&\'—-]'
    for word in text:
        word = word.strip(punct)
    reply = []
    with open('words.txt', 'r', encoding = 'utf-8') as f:
        words = f.read()
        text_wo_punct = re.sub(punct,'', words.lower())  
        new_words = text_wo_punct.strip().split()  
    for tword in text:
        new_grs = []
        ana_tword = morph.parse(tword)[0]
        word = random.choice(new_words)
        ana_random_word = morph.parse(word)[0]
        while ana_random_word.tag.POS != ana_tword.tag.POS:
            word = random.choice(words)
            ana_random_word = morph.parse(word)[0]
        else:
            ana_tag_to_grs = re.sub(' ', ',', str(ana_tword.tag)) 
            grs = ana_tag_to_grs.split(',')
            for gr in grs[1:]:
                try:
                    ana_word = ana_random_word
                    ana_word = ana_word.inflect({gr})
                    if ana_word != None:
                        new_grs.append(gr)
                except AttributeError:
                    pass
            for gr in new_grs:
                final_word = ana_random_word.inflect({gr})
                reply.append(final_word.word)        
    new_sentence = ' '.join(reply) 
    return render_template('result.html', sentence=new_sentence)     
 
if __name__ == '__main__':
    app.run(debug=True)
