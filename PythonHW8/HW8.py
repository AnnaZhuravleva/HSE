with open (r"C:\Users\Анна\Documents\GitHub\prog\PythonHW8\words.csv", 'r', encoding = 'utf-8') as text:
    mas = []
    for line in text:
        words = line.split(',')
        for word in words:
            mas.append(word)
words = {}

for i in mas:
    word = i.split(';')
    words[word[0].strip()] = word[1].strip()


for key in words:
    print(key, '...')
    p = 3
    for i in range (3):
        if input() != words[key]:
            p -= 1
            print('Осталось', p, 'попыток')
            if p == 0:
                print('Вы не угадали слово')
        else:
            print ('Ура! Вы угадали слово!')
            break
       
       
            
    


        





