def opening(name):
    with open (name, 'r', encoding = 'utf-8') as f:
        count = 0
        for line in f:
            if line !='  </teiHeader>\n':
                count += 1
            else:
                break
    return count
def writing():
    count = opening(name)
    with open('2.txt', 'w', encoding = 'utf-8') as f:
        f.write(str(count))
        
name = r'C:\Users\student\Desktop\1.xml'
writing()
import re
with open (name, 'r', encoding = 'utf-8') as f:
    content = f.read()
    arr = re.findall(r'(<w lemma=".*?" type="(.*?)">.*?</w>)', content)
    d = {}
    for i in arr:
        d[i[1]] = content.count(i[1])
with open ('3.txt', 'w', encoding = 'utf-8') as f:
    for key in d:
        a = str(key) + ' ' + str(d[key]) + '\n'
        f.write(a)
        
   
        
