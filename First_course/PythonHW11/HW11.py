with open (r'C:\Users\Анна\Documents\GitHub\prog\PythonHW11\lingva.html', 'r', encoding = 'utf-8') as f:
    content = f.read()
import re
article = re.sub(u'язык((а(х|ми?)?|у|о(м|в)|и|е)?[\s.,— ''""<>?!»():-;])', 'шашлык\\1', content) 
article2 = re.sub(u'Язык((а(х|ми?)?|у|о(м|в)|и|е)?[\s.,— ''""<>?»!():-;])', 'Шашлык\\1', article) 
with open ('new.txt', 'w', encoding='utf-8') as f: 
    f.write(article2)



