#6. какова частотность слов с приставкой omni- в тексте и частотность слов без приставки omni-
#(то есть, например, сообщает, сколько раз в тексте встречается слово omnibenevolent и
# сколько раз встречается слово benevolent, и так для всех слов с приставкой omni-)
def reading():
    with open (r"C:\Users\Анна\Documents\ФиКЛ\PythonHW7\omni.txt", 'r', encoding='utf8') as text:
        mas = []
        for line in text:
            words = line.split()
            for word in words:
                word = word.strip(',.;"()-!?')
                mas.append(word.lower())
        return(mas)

def omni_counting():
    s = 0
    omni = []
    for word in reading():
        if word[:4] == 'omni':
            s += 1
            if word not in omni:
                omni.append(word)
    print (s,'words with OMNI-')
    p = 0
    for word in omni:
        without_omni = []
        w2 = word[4:]
        if w2 not in without_omni:
            without_omni.append(w2)
            p += int(reading().count(w2))
    print(p, 'words without OMNI-')
    
omni_counting()   
 
#P.S. В "гордости и предубеждении" нет ни одного слова с приставкой omni, поэтому создала другой файл


