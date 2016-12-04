#Вариант 6. Открыть файл и посчитать процент слов с заглавной буквы
total = 0
upletters = 0
with open(r'C:\Users\Анна\Documents\GitHub\prog\PythonHW5\text.txt','r',encoding='utf8') as f:
    text = f.read()
    words = text.split()
    for item in words:
       total += 1
       for letter in item:
           if letter.isupper():
               upletters += 1
           else:
               continue
print("Количество слов в тексте: ",total)
print('Количество слов с заглавной буквы',upletters)
print("Процент слов в тексте, начинающихся с заглавной буквы: ", upletters/total,'%')

    
            
            
