import re
m1 = 'загруж(у|(енн?(ы(й|е|х|ми?)?|о(го|му?|е|й)?|ую|а)?))(с(я|ь))?'
m2 = 'загруз(и(т|шь|м|т(ь|е)?|л(а|о|и)?)?(в(ш(и(й|ми?|х)|е(го|му?|е|й)))?)?|ят)(с(я|ь))?'

with open (r"C:\Users\Анна\Documents\GitHub\prog\PythonHW9\re.txt",'r', encoding='utf-8') as f:
    mas = []
    for line in f:
        words = line.split()
        for word in words:
            word = word.strip(',.;"()-!?')
            mas.append(word.lower())
arr = []
for i in mas:
    a = re.search(m1,i)
    b = re.search(m2,i)
    if a != None and len(a.group()) == len(i):
        if a.group() not in arr:
            arr.append(a.group())
            print(a.group())
    if b != None and len(b.group()) == len(i):
        if b.group() not in arr:
            arr.append(b.group())
            print(b.group())
