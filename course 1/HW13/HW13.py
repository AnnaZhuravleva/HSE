import os
import re


def folder_opening(big_folder):
    names = [item for item in os.listdir(big_folder) if os.path.isfile(item) and re.search
    ('[^.]*\..*?[,._?<>''""!-()].*?', str(item)[::-1])]
    return len(names)


def all_files(big_folder):
    files = [item[::-1] for item in os.listdir(big_folder) if os.path.isfile(item)]
    all_files = []
    for item in files:
            all_files.append((re.sub(u'([^.]*\.)?(.*)', u'\\2', str(item))[::-1]))
    for item in os.listdir(big_folder):
        if os.path.isdir(item):
            all_files.append(item)      
    all_files_new = []
    for item in all_files:
        if item not in all_files_new:
            all_files_new.append(item)
    # all_files_new = [item for item in all_files if item not in all_files_new] - почему-то не выполняется условие not in all_files_new
    return all_files_new


print('Найдено', folder_opening('.'), 'файлов, название которых содержит знаки препинания')
print('Все файлы:', all_files('.'))
