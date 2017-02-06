def content(name):
    with open (name, 'r', encoding = 'utf-8') as f:
        content = f.read()
        return content
name = r"C:\Users\Анна\Documents\GitHub\prog\PythonHW10\Squirrels.html"
import re
reg = u'(<td\s+align="right">Отряд:</td>\n<td\s+align="left"><a\\s+href="/wiki/(.*)">(.*)</a></td>)'
link = re.search(reg, content(name))
link = ((re.search(('title="(.*)"'),link.group())).group()).strip('title="')
print("Отряд", link)




