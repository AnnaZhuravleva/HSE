
# coding: utf-8


# coding: utf-8

# In[1]:


import urllib.request, json, sqlite3
import matplotlib.pyplot as plt   


# In[2]:


conn = sqlite3.connect("vk1111.db") 
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS posts
                (ID text, post text, length text, author text)
                """)
conn.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS comments
                (PostID text, PostLength text, CommentLength text)
                """)
conn.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS comments_and_authors
                (CommentID text,length, author)
                """)

conn.commit()
def writing_into_db(ID,post,lenght,author):   
    m = [ID,post,lenght,author]
    cursor.execute("INSERT INTO posts VALUES (?,?,?,?)", m)
    conn.commit()
def comments_and_authors(ID,length,author):
    m = [ID,length,author]
    cursor.execute("INSERT INTO comments_and_authors VALUES (?,?,?)", m)
    conn.commit()
def writing_comments(ID,post,comment):
    m = [ID,post,comment]
    cursor.execute("INSERT INTO comments VALUES (?,?,?)", m)
    conn.commit()    


# In[3]:


offsets = [0,1]
for off in offsets:
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=&domain=dfzwe4&v=5.74&access_token=364952c2364952c2364952c23b362bf79f33649364952c26caca3158b4898baf5a9e2ba&count=100&offset='+ str(off))
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    data = json.loads(result)
    for i in range(0,100):
        post = data['response']['items'][i]['text']
        ID = data['response']['items'][i]['id']
        length = len(post.split(' '))
        author = data['response']['items'][i]['from_id'] 
        writing_into_db(ID,post,length,author)
cursor.execute('SELECT * FROM posts')
print(cursor.fetchall())


# In[4]:


cursor.execute('SELECT ID, length FROM posts')
l = cursor.fetchall()
for i in l: 
    req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-40232010&post_id='+i[0]+'&v=5.74&access_token=364952c2364952c2364952c23b362bf79f33649364952c26caca3158b4898baf5a9e2ba&count=100')
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    data = json.loads(result)
    print(data['response']) 
    number = data['response']['count']
    if number >> 100:
        offsets = [0,100,200,300]
        for off in offsets:
            req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-40232010&post_id='+i[0]+'&v=5.74&access_token=364952c2364952c2364952c23b362bf79f33649364952c26caca3158b4898baf5a9e2ba&count=100&offset='+str(off))
            response = urllib.request.urlopen(req) 
            result = response.read().decode('utf-8')
            data = json.loads(result)
            print(data['response'])
    comments = 0            
    for item in data:
        for a in range (0,int(data['response']['count'])):
            comment = data['response']['items'][a]['text']
            ID = data['response']['items'][a]['id']
            comment_length = len(comment.split(' '))
            author = data['response']['items'][a]['from_id'] 
            comments += int(comment_length)
            print(comment,ID,comment_length,author)
            comments_and_authors(ID,comment_length,author)
    if number != 0:
        writing_comments(str(i[0]),str(i[1]),str(comments//number))
    #print('\n\nI ',i,'\n.\nlenght',str(comments//number),'\n________\n')
    


# In[5]:


l= {}
for raw in cursor.execute('SELECT PostLength, CommentLength FROM comments ORDER BY PostID'):
    l[raw[0]] = raw[1] 
lp = [a for a in sorted(l)] 
lc = [l[a] for a in sorted(l)]
plt.bar(range(len(lp)),lc)
plt.title("Соотношение длины поста (в словах) и средней длины комментариев (в словах)")
plt.xlabel("Длина поста (в словах)")
plt.ylabel("Средняя длина комментариев (в словах)")
plt.savefig('posts&comments.png', format='png', dpi=100)
plt.show()


# In[6]:


cursor.execute('SELECT * FROM comments_and_authors')
print(cursor.fetchall())


# In[ ]:


cursor.execute("""CREATE TABLE IF NOT EXISTS comments_age_cities
                (comment_length text, city text, age text)
                """)
conn.commit()
cursor.execute('SELECT length, author FROM comments_and_authors')
pq = cursor.fetchall()
for i in pq:
    req = urllib.request.Request('https://api.vk.com/method/users.get?v=5.23&user_ids={}&fields=bdate,city'.format(str(i[1])))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    print(data['response'])
    if 'bdate' in data['response']:
        if data_p['response'][0]['bdate'] != '':
            date = data['response'][0]['bdate']
            print(date)
    if 'city' in data['response']:
        if data_p['response'][0]['city'] != '':
            city = data['response'][0]['city']['title']
            print(city)
    else:
        city = ''
    print('\n---------------\n')
    #cursor.execute("INSERT INTO comments_age_cities VALUES (?,?,?)", (str(i[0]),city,age))
    conn.commit()  


# In[ ]:


#cursor.execute("SELECT * FROM comments_age_cities")
#print(cursor.fetchall())


