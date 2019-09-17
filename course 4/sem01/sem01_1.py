# Поисковой модуль по коллекции документов - субтитров сериала Friends
# json.txt - содержит словарь, где ключ - имя файла, а значения - все слова,
# содержащиеся в файле
# invert_json.txt - Инвертированный индекс (слова - имя файла,
# в которых содержатся эти слова)
# Перезаписать эти файлы заново можно при помощи метода _indexing()
# По умолчанию папка с субтитрами лежит в той же папке, что и питоновский файл
# Если субтитров там не находится, то просит указать путь к папке
# Все слова приведены к начальной форме с помощью pymorphy2

import os
import re
import json
import math
import collections
import pymorphy2


pmm = pymorphy2.MorphAnalyzer()


class InfoSearch:

    def __init__(self):
        try:
            self.data = self.loads('json.txt')
            self.invert_idx = self.loads('invert_json1.txt')
            self._filenames = self.filenames()
        except FileNotFoundError:
            print('loading..')
            self._filenames = self.filenames()
            self.indexing()
            self.data = self.loads('json.txt')
            self.invert_idx = self.loads('invert_json1.txt')

    def filenames(self):
        curr_dir = os.path.join(os.getcwd(), 'friends')
        if not os.path.exists(curr_dir) or not os.path.isdir(curr_dir):
            curr_dir = input('Введите верный путь к папке friends: ')
        for root, dirs, files in os.walk(curr_dir):
            for name in files:
                filename = os.path.join(root, name)
                if filename.endswith('.txt'):
                    yield filename

    def preprocessing(self):
        for filename in self._filenames:
            with open(filename, 'r', encoding='utf-8') as f:
                tmp = f.read().split()
                tmp = [re.sub(r"[^А-Яа-я-]+", "", word).lower() for
                       word in tmp if re.match('[А-Яа-я]', word)]
                tmp = [pmm.normal_forms(word)[0] for word in tmp]
                yield tmp

    def indexing(self):
        js = {}
        files = self.preprocessing()
        for filename, text in zip(self._filenames, files):
            js[filename.split('\\')[-1]] = text
        invert_index = collections.defaultdict(list)
        for filename in js:
            for word in js[filename]:
                if [filename, 0] not in invert_index[word]:
                    invert_index[word].append([filename, 0])
        nb = len(js)
        for word in invert_index:
            for doc in invert_index[word]:
                doc[1] = round(
                    (js[doc[0]].count(word)/len(js[doc[0]])) *
                    (math.log10(nb/sum([1 for i in js if word in js[i]]))), 5)
        invert_index = {word: {k[0]: k[1] for k in invert_index[word]}
                        for word in invert_index}

        with open('json.txt', 'w', encoding='utf-8') as outfile:
            json.dump(js, outfile, ensure_ascii=False)
        with open('invert_json1.txt', 'w', encoding='utf-8') as outfile:
            json.dump(invert_index, outfile, ensure_ascii=False)
        return None

    def loads(self, path):
        with open(path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    def relevant(self, request):
        result = collections.defaultdict(int)
        tmp = request.split()
        tmp = [re.sub(r"[^А-Яа-я-]+", "", word).lower() for word in tmp
               if re.match('[А-Яа-я]', word)]
        query = [pmm.normal_forms(word)[0] for word in tmp]
        for key in self.data:
            for word in query:
                if word in self.data[key]:
                    result[key] += self.invert_idx[word][key]
        result = {key: round(result[key], 5) for key in result}
        return sorted(result.items(), key=lambda k: k[1], reverse=True)

    def search(self):
        while True:
            print('Если ничего не хотите искать, нажмите 0')
            query = input('Введите запрос: ')
            if query == '0':
                break
            result = self.relevant(query)
            for item in result:
                print(f'{item[0]} - {item[1]} tf-idf')
        return None

    def stats(self):
        tmp = {k[0]: round(sum(k[1].values()), 5)
               for k in self.invert_idx.items()}
        tmp = sorted(tmp.items(), key=lambda k_v: k_v[1], reverse=True)
        monika = collections.defaultdict(int)
        for episode in self.invert_idx['моника']:
            monika[episode.split(' ')[2][0]] += \
                self.invert_idx['моника'][episode]
        monika = {k: round(v, 5) for k, v in monika.items()}
        monika = sorted(monika.items(), key=lambda k: round(k[1], 5),
                        reverse=True)
        chandler = collections.defaultdict(int)
        for episode in self.invert_idx['чендлер']:
            chandler[episode.split(' ')[2][0]] += \
                self.invert_idx['чендлер'][episode]
        chandler = {k: round(v, 5) for k, v in chandler.items()}
        chandler = sorted(chandler.items(),
                          key=lambda v: round(v[1], 5), reverse=True)
        heroes = {hero: round(sum([self.invert_idx[hero][key] for key in
                                   self.invert_idx[hero]]), 5) for hero in
                  ['моника', 'рэйчел', 'чендлер', 'фиби', 'джоу', 'росс']}
        heroes = sorted(heroes.items(), key=lambda k_v: k_v[1], reverse=True)
        all_docs = [item for item in self.invert_idx.keys()
                    if len(self.invert_idx[item]) == 165]
        stats = f'======================================================' \
            f'================================\n' \
            f'Самое частотное слово в коллекции - {tmp[0][0]}: ' \
            f'его Tf-Idf равен {tmp[0][1]} .\n' \
            f'Самое редкое слово в коллекции - ' \
            f'{tmp[-1][0]}: его Tf-Idf равен {tmp[-1][1]} \n' \
            f'Во всех документах коллекции встречаются такие слова: ' \
            f'{all_docs}.\n' \
            f'Самый популярный сезон для Моники - {monika[0][0]}.\n' \
            f'Сравним Tf-Idf по каждому сезону: {monika}\n' \
            f'Самый популярный сезон для Чендлера - {chandler[0][0]}.\n' \
            f'Сравним Tf-Idf по каждому сезону: {chandler}\n' \
            f'Самый популярный герой - {str(heroes[0][0]).title()}. ' \
            f'Сравним tf-idf для всех героев:\n{heroes}\n' \
            f'==========================================================' \
            f'============================\n'
        print(stats)
        return stats

    __repr__ = stats
    __str__ = __repr__


if __name__ == '__main__':
    friends = InfoSearch()
    # friends.indexing()
    friends.stats()
    friends.search()

