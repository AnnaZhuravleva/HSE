import urllib.request,re,os,html.parser, csv

def download_page(pageUrl): #Загрузка страницы
    req = urllib.request.Request(pageUrl)
    with urllib.request.urlopen(req) as page:
        html = page.read().decode('utf-8')
    return html #HTML - текст с тэтагми

def creating_folders(year): #создаем папки
    path_plain = os.path.join('plain',year)
    if not os.path.exists(path_plain):
        os.mkdir(path_plain)
        print(path_plain)
    path_mystem_plain = os.path.join('mystem',year)
    if not os.path.exists(path_mystem_plain):
        os.mkdir(path_mystem_plain)
    path_mystem_xml = os.path.join('mystemXml',year)
    if not os.path.exists(path_mystem_xml):
        os.mkdir(path_mystem_xml)
    return path_plain  

def collecting_pages(commonUrl):#собираем массив со ссылками
    commonRegPostTitle = '<a href="/ural/{0}/{1}/(.*?).html">(.*?)</a>'
    pages = {}
    for i in range(2016,2018):
        pageUrl_1= commonUrl + str(i)+ '/'
        year = (str(i))
        folder = creating_folders(year)
        for n in range (1,10):
            pageUrl_2 = pageUrl_1 + str(n)
            text = download_page(pageUrl_2)
            validReg = commonRegPostTitle.format(str(i),str(n))
            regPostTitle = re.compile(validReg, flags= re.DOTALL)
            titles = regPostTitle.findall(text)
            for title in titles[1:10]:
                pageUrl_3 = pageUrl_2 + '/' + title[0] + '.html'
                file_name = html.parser.HTMLParser().unescape(title[0])
                pages[pageUrl_3] = year, folder, file_name #массив: URL ссылка - год,  путь к папке,название статьи
    return pages
    
def metadate(html):#собираем метаданные
    author = re.search('<div class="authors">\s*.*?([^<>]*?)</a>',html) 
    if author: 
        author = ['@au ',str(author.group(1))]
    else: 
        author = ['@au ','Не указан']
    title = ['@ti ',str(re.search('<div class="col-xs-9">\s*<h1>(.*?)</h1>', html).group(1))]
    date = re.search('Опубликовано в журнале:\s*<a href="/ural/">Урал</a>\s*<a href="/ural/.*?">(.*?),(.*?)</a>', html)
    year = str(date.group(1))
    date = ['@da ',str(date.group(2) + '.' + date.group(1))]
    topic = re.search('<div class="col-xs-9">\s*<h1>(.*?)</h1>\s*<h4>(.*?)</h4>', html)
    if topic:
        topic = ['@topic ',str(topic.group(2))]
    else:
        topic = ['@topic ','Не указан']       
    metadate = [author,title,date,topic,year]  
    return metadate

    
  
def tegs_cleaning (html): #чистим от тегов
    regTag = re.compile('<.*?>', re.DOTALL)  
    regScript = re.compile(u'<script.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)  
    clean = regScript.sub('', html)
    clean = regComment.sub("", clean)
    clean = regTag.sub("", clean)
    return clean #текст без тэгов

def plain_text(html,path,file):
    file_name = '{0}.txt'
    with open (os.path.join(path,file_name.format(file)), 'a', encoding = 'utf-8') as f:
        for date in (metadate(html)[0:4]):
            f.write(date[0]+date[1]+'\n')
        f.write('@url ' + str(page)+'\n')
        f.write(tegs_cleaning(html))
    return file_name.format(file)
    
    



def mystem_plain():
    for root, dirs, files in os.walk ('plain'):
        for f in files:
            goalDir = root.replace('plain', 'mystem')
            mystem_plain = mystem + ' ' + root + os.sep + f + ' ' + goalDir+  os.sep + f + ' -cid --format text'
            os.system(mystem_plain)
def mystem_xml():
    for root, dirs, files in os.walk ('plain'):
        for f in files:
            goalDir = root.replace('plain', 'mystemXml')
            mystem_plain = mystem + ' ' + root + os.sep + f + ' ' + goalDir+  os.sep + f.replace('.txt', '.xml') + ' -cid --format xml'
            os.system(mystem_plain)
            
os.mkdir('plain')
os.mkdir('mystemXml')
os.mkdir('mystem')
commonUrl = 'http://magazines.russ.ru/ural/'
mystem = r'mystem.exe'
columns = ["path",'author','sex','birthday','header','created','sphere','genre_fi','type','topic','chronotop','style','audience_age',\
    'audience_level','audience_size','source','publication','publisher','publ_year','medium','country','region','language']
with open('metadata.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(columns)

pages = collecting_pages(commonUrl)
for page in pages:
    print(page)
    html = download_page(page)
    file = pages[page][2]
    path = pages[page][1]
    name = plain_text(html,path,file)
    meta = metadate(html)
    row_csv = [path, meta[0][1],'','',meta[1][1],meta[2][1],'публицистика','','',meta[3][1],'','нейтральный','н-возраст','н-уровень','областная',\
               page,'Урал','',meta[4],'газета','Россия','Свердловская область','ru']
    with open ('metadata.csv', 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(row_csv) 

mystem_plain()
mystem_xml()
    
    
