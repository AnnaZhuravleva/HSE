import os, re
def folder_opening(big_folder):
    names = [item for item in os.listdir(big_folder) if os.path.isfile(item) and re.search('[^.]*\..*?[,._?<>''""!-()].*?',str(item)[::-1])]
    all_files = []
    all_files = [item for item in os.listdir(big_folder) if item not in all_files]
    print('Все файлы и папки:',all_files)
    return len(names)
print('Найдено',folder_opening('.'), 'файлов, название которых содержит знаки препинания')
  

        
    
