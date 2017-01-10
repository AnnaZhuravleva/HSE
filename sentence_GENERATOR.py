#6. Текст должен состоять из 5 предложений разных типов
#(утвердительные, вопросительные, отрицательные, условные, побудительные) на
#изучаемом вами языке (французский, испанский).
#Типы предложений должны выводиться в случайном порядке.
import random
def nouns():
    f = open (r'D:\Desktop\Аня\sentence_generator\nouns.txt','r', encoding = 'UTF-8')
    a = f.read()
    a = a.split()
    arr = []
    for w in a:
        arr.append(w)    
    return random.choice(arr)
    f.close()

def adjectives():
    f = open (r'D:\Desktop\Аня\sentence_generator\adjectives.txt','r', encoding = 'UTF-8')
    a = f.read()
    a = a.split()
    arr = []
    for w in a:
        arr.append(w)
    return random.choice(arr) + ' ' + nouns ()

def verbs():
    f = open (r'D:\Desktop\Аня\sentence_generator\verbs.txt','r', encoding = 'UTF-8')
    a = f.read()
    a = a.split()
    arr = []
    for w in a:
        arr.append(w)    
    return random.choice(arr)
    f.close()

def adverbs():
    f = open (r'D:\Desktop\Аня\sentence_generator\adverbs.txt','r', encoding = 'UTF-8')
    a = f.read()
    a = a.split()
    arr = []
    for w in a:
        arr.append(w)    
    return random.choice(arr)
    f.close()
    
def assertion():
    return(adjectives()) + ' ' + (verbs()) + 't' + ' ' + 'une ' + (adjectives()) + ' ' + (adverbs())

def sentence():
    return 'La ' + (assertion()) + '.'

def negation():
    return 'La ' + (adjectives()) + ' ' + 'ne' + ' ' + (verbs()) + 't' + ' ' + 'pas ' + 'une ' + (adjectives()) + ' '\
           + (adverbs()) + '.'

def question():
    return 'La ' + (adjectives()) + ' ' + (verbs()) + 't' + '-elle ' + 'une ' + (adjectives()) + ' ' + (adverbs()) + '?'

def conditions ():
    return 'Si ' + (assertion()) + ', ' + (assertion()) + '.'

def imperative():
    a = str(verbs())
    return (a.capitalize() + 's' + ' ' + 'une ' + (adjectives()) + ' ' + (adverbs()) + '!')

mas = [(sentence()),(negation()),(question()),(conditions ()),(imperative ())]
mass = []
for i in range (len(mas)):
    for item in mas:
        randitem = random.choice(mas)
        if randitem not in mass:
            mass.append(randitem)
            print(randitem)


    
    
    

    


    
    


    
    
    
