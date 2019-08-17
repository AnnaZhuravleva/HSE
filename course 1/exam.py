import os,re
def counting_sentences(file):
    sentences = re.findall('</se>', file)
    return len(sentences)
 
def opening_folders(folder): ##читает файлы в папке
    path = folder
    dic = {}
    for file in os.listdir(folder):
        with open ((os.path.join(folder, file))) as f:
            text = f.read()
            number = int(counting_sentences(text))
            dic[file] = number
    return dic

def writing_table(dic):
    with open ('number_of-sentences.txt', 'w', encoding = 'utf-8') as f:
        for file in dic:
            f.writelines(file + '\t' + str(dic[file]) + '\n')

def author_and_topic(folder):
    path = folder
    for file in os.listdir(folder):
        with open ((os.path.join(folder, file))) as f:
            text = f.read()
            reg1 = '(content="(.*)" name="author")'
            reg2 = '(content="(.*)" name="topic")'
            for i in range (1):
                for i in re.findall(reg1, text):
                    author = i[1]
                for i in re.findall(reg2, text):
                    topic = i[1]
    

            
            

writing_table(opening_folders(r'C:\Users/student/Desktop/news/'))
author_and_topic(r'C:\Users/student/Desktop/news/')


    
            
            
