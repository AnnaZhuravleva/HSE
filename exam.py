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

writing_table(opening_folders(r'C:\Users/student/Desktop/news/'))



    
            
            
