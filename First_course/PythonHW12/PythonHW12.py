def opening(file):
    with open(file, 'r', encoding = 'utf-8') as f:
        f = f.read()
        sentences = f.split('.')
        mas = []
        for sentence in sentences:
            sentence = sentence.split('!')
            for i in sentence:
                i = i.split('?')
                for a in i:
                    mas.append(a)        
        return mas
for sentence in opening(r"C:\Users\Анна\Documents\GitHub\prog\PythonHW12\text.txt"):
    words = sentence.split()
    new_words = [word.strip('.,!?/-;:''""«»—()') for word in words if len(words) > 10]
    print(new_words)
    lenght = 0
    for word in new_words:
        lenght += len(word)
    if new_words:
        template = 'Это предложение со словами длины {:.1f}'
        print (template.format(lenght/len(new_words)))

