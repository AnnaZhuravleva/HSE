import urllib.request 
req = urllib.request.Request('http://magazines.russ.ru/ural/')
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
import re
regPostTitle = re.compile('<strong.*?</strong>', flags= re.DOTALL)
titles = regPostTitle.findall(html)
new_titles = []
regTag = re.compile('<.*?>', re.DOTALL)
regSpace = re.compile('\s{2,}', re.DOTALL)
for t in titles:
    clean_t = regSpace.sub("", t)
    clean_t = regTag.sub("", clean_t)
    new_titles.append(clean_t)
with open ('Заголовки.txt', 'w', encoding = 'utf-8') as f:
    for t in new_titles:
        f.write(t + '\n')
