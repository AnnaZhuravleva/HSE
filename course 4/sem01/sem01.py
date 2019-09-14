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
import collections
import pymorphy2
import random


pmm = pymorphy2.MorphAnalyzer()


class InfoSearch:

    def __init__(self):
        try:
            self.data = self.loads('json.txt')
            self.invert_idx = self.loads('invert_json.txt')
        except FileNotFoundError:
            print('loading..')
            self._filenames = self.filenames()
            self.indexing()
            self.data = self.loads('json.txt')
            self.invert_idx = self.loads('invert_json.txt')

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
                if filename not in invert_index[word]:
                    invert_index[word].append(filename)

        with open('json.txt', 'w', encoding='utf-8') as outfile:
            json.dump(js, outfile, ensure_ascii=False)
        with open('invert_json.txt', 'w', encoding='utf-8') as outfile:
            json.dump(invert_index, outfile, ensure_ascii=False)
        return None

    def loads(self, path):
        with open(path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    def relevant(self, request, data):
        result = collections.defaultdict(int)
        tmp = request.split()
        tmp = [re.sub(r"[^А-Яа-я-]+", "", word).lower() for word in tmp
               if re.match('[А-Яа-я]', word)]
        query = [pmm.normal_forms(word)[0] for word in tmp]
        for key in data:
            for word in query:
                if word in data[key]:
                    result[key] += 1
        return sorted(result.items(), key=lambda k: k[1], reverse=True)

    def search(self):
        while True:
            print('Если ничего не хотите искать, нажмите 0')
            query = input('Введите запрос: ')
            if query == '0':
                break
            result = self.relevant(query, self.data)
            for item in result:
                print(f'{item[0]} - {item[1]} соответствий в коллекции')
        return None

    def stats(self):
        tmp = sorted(self.invert_idx.items(), key=lambda k_v: len(k_v[1]),
                     reverse=True)
        rare = [item[0] for item in tmp if len(item[1]) == 1]
        monika = collections.defaultdict(int)
        for episode in self.invert_idx['моника']:
            monika[episode.split(' ')[2][0]] += 1
        monika = sorted(monika.items(), key=lambda k: k[1], reverse=True)[0][0]
        chandler = collections.defaultdict(int)
        for episode in self.invert_idx['чендлер']:
            chandler[episode.split(' ')[2][0]] += 1
        chandler = sorted(chandler.items(),
                          key=lambda v: v[1], reverse=True)[0][0]
        heroes = {hero: len(self.invert_idx[hero]) for hero in
                  ['моника', 'рэйчел', 'чендлер', 'фиби', 'джоу', 'росс']}
        heroes = sorted(heroes.items(), key=lambda k_v: k_v[1], reverse=True)
        stats = f'======================================================' \
            f'================================\n' \
            f'Самое частотное слово в коллекции - {tmp[0][0]}: ' \
            f'оно встречается в {len(tmp[0][1])} документах.\n' \
            f'Самые редкие слова в коллекции - {random.choice(rare)}: ' \
            f'оно встречается только в 1 документе.\n' \
            f'Во всех документах коллекции встречаются такие слова: ' \
            f'{[item[0] for item in tmp if len(item[1]) == 165]}.\n' \
            f'Самый популярный сезон для Моники - {monika}.\n' \
            f'Самый популярный сезон для Чендлера - {chandler}.\n' \
            f'Самый популярный герой - {str(heroes[0][0]).title()}: ' \
            f'его упоминают в {heroes[0][1]} сериях\n' \
            f'==========================================================' \
            f'============================\n'
        print(stats)
        return stats

    __repr__ = stats
    __str__ = __repr__


if __name__ == '__main__':
    friends = InfoSearch()
    friends.stats()
    friends.search()
