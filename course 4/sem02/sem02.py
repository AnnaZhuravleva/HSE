from sklearn.feature_extraction.text import TfidfVectorizer
from math import log10
import pandas as pd
import numpy as np
import pymorphy2
import logging
import time
import csv
import sys
import re
import os


pmm = pymorphy2.MorphAnalyzer()
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
root.addHandler(handler)


class Data:

    def __init__(self, k=2.0, b=0.75, top=5000):
        self.k = k
        self.b = b
        self.top = top
        self.data = pd.read_csv('collection.csv')
        self.collection = self.data['question2'][:top]
        self._length = len(self.collection)
        self.docs = [str(doc).split(' ') for doc in self.collection]
        self.avg = np.mean([len(doc) for doc in self.docs]).round(5)
        self.vectorizer = TfidfVectorizer()
        self.model = self.vectorizer.fit(self.collection)
        self.matrix = self.vectorizer.transform(self.collection)
        self.dictionary = self.vectorizer.get_feature_names()
        name = re.sub(r'\.', '', f'matrix_b{self.b}_{top}') + '.npy'
        if os.path.isfile(name):
            self.bm25_matrix = np.load(name)
        else:
            self.bm25_matrix = self.bm25_build_matrix(name)

    def bm25(self, doc, query, n, ld):
        score = 0.0
        for number, word in enumerate(query):
            idf = log10((self._length - n[number] + 0.5) / (n[number] + 0.5))
            tf = doc.count(word) / ld
            score += idf * (tf * (self.k + 1.0)) / (
                    tf + self.k * (1 - self.b + (self.b * ld / self.avg)))
        return score

    def bm25_build_matrix(self, name):
        logging.info('wait...')
        bm25_matrix = np.zeros(self.matrix.shape)
        n = [sum([1 for doc in self.docs if word in doc]) for word in
             self.dictionary]
        for idw, word in enumerate(self.dictionary):
            for idd, doc in enumerate(self.docs):
                bm25_matrix[idd, idw] = self.bm25(
                    doc, [word], [n[idw]], len(doc))
            # logging.info(f'{idw} from {len(self.dictionary)}')
        np.save(name, bm25_matrix)
        logging.info('matrix saved')
        return bm25_matrix

    def normalize(self):  # запускаем, если еще нет файла collection.csv
        data0 = pd.read_csv('quora_question_pairs_rus.csv')
        with open('collection.csv', 'w', newline='', encoding='utf8') as w:
            writer = csv.writer(w, delimiter=',')
            writer.writerow(['question', 'question2'])
            for idx, doc in enumerate(self.docs):
                words = [w.strip(r',\.\"!–?-\'\"\(\)\"-::—;)(\«\»\W')
                         for w in doc]
                words = [pmm.normal_forms(word)[0] for word in words]
                writer.writerow([data0['question2'][idx], ' '.join(words)])


class BM25(Data):

    def __init__(self, *args, **kwargs):
        logging.info('Initializing...')
        super().__init__(*args, **kwargs)
        self.test_data = pd.read_csv('quora_question_pairs_rus.csv')[:self.top]
        self.queries = \
            [[i, j] for i, j in enumerate(self.test_data['question1'])
             if self.test_data['is_duplicate'][i] == 1]

    def search_iter(self, query, top=5):
        query = [w.strip(r',\.\"!–?-\'\"\(\)\"-::—;)(\«\»\W')
                 for w in query.split()]
        query = [pmm.normal_forms(word)[0] for word in query]
        n = [sum([1 for doc in self.docs if word in doc]) for word in query]
        res = []
        for i, d in enumerate(self.docs):
            score = self.bm25(d, query, n, len(d))
            if score > 0.0:
                res.append([i, score])
        res = sorted(res, key=lambda x: x[1], reverse=True)
        return res[:top]

    def search_matrix(self, query, top=5):
        query = [w.strip(r',\.\"!–?-\'\"\(\)\"-::—;)(\«\»\W')
                 for w in query.split()]
        query = [pmm.normal_forms(word)[0] for word in query]
        vector = np.zeros((len(self.dictionary), 1))
        for i, j in enumerate(self.dictionary):
            vector[i, 0] = 1 if j in query else 0
        result = self.bm25_matrix.dot(vector)
        res = [[i, j] for i, j in enumerate(result)]
        res = sorted(res, key=lambda x: x[1], reverse=True)
        return res[:top]

    def test_time(self, number=10000):
        logging.info(f'Сравним время работы двух поисковиков на {number} '
                     f'запросах, b = {self.b}')
        start_iter = time.time()
        for item in self.queries[:number]:
            self.search_iter(item[1])
        end_iter = time.time()
        logging.info(f'Время работы первого поисковика -'
                   f' {end_iter - start_iter}')
        start_matrix = time.time()
        for item in self.queries[:number]:
            self.search_matrix(item[1])
        end_matrix = time.time()
        logging.info(f'Время работы второго поисковика -'
                     f' {end_matrix - start_matrix}')
        return [end_iter - start_iter, end_matrix - start_matrix]

    def test_query(self, query='рождественские каникулы', top=10):
        logging.info(f'Выводим результаты по запросу {query}, b = {self.b}')
        logging.info('Первый поисковик')
        for i, j in enumerate(self.search_iter(query, top)):
            text = self.test_data['question2'][j[0]]
            logging.info(f'{i}.\tText_id: {j[0]},\tscore: {j[1].round(8)},'
                         f'\ttext: {text}')
        logging.info('Второй поисковик')
        for i, j in enumerate(self.search_matrix(query, top)):
            text = self.test_data['question2'][j[0]]
            logging.info(f'{i}.\tText_id: {j[0]},\tscore:'
                         f' {j[1][0].round(8)},\ttext: {text}')
        return

    def test_accuracy(self, number=1000, top=5):
        logging.info(f'Сравним точность двух поисковиков на {number} '
                     f'запросах при b = {self.b}, top = {top}')
        queries = self.queries[:number]
        accuracy_iter = 0
        accuracy_matrix = 0
        for q1 in queries:
            res_iter = [x[0] for x in self.search_iter(query=q1[1], top=top)]
            accuracy_iter += int(q1[0] in res_iter)
        accuracy_iter = "{:.0%}".format(accuracy_iter / number)
        logging.info(f'Точность первого поисковика - {accuracy_iter}')
        for q1 in queries:
            res_matrix = [x[0] for x in self.search_iter(query=q1[1], top=top)]
            accuracy_matrix += int(q1[0] in res_matrix)
        accuracy_matrix = "{:.0%}".format(accuracy_matrix / number)
        logging.info(f'Точность второго поисковика - {accuracy_matrix}')

        return


if __name__ == '__main__':
    bm25 = BM25(top=12000)  # В скобках указываем количество документов
    # bm15 = BM25(b=0, top=12000)
    # bm11 = BM25(b=1, top=12000)
    bm25.test_time(120)  # В скобках указываем количество запросов
    bm25.test_query('рождественские каникулы', top=10)  # В скобках указываем
    # количество результатов
    # bm15.test_query('рождественские каникулы', top=5)
    # bm11.test_query('рождественские каникулы', top=5)
    bm25.test_accuracy(number=120, top=5)
    # bm15.test_accuracy(number=120, top=5)
    # bm11.test_accuracy(number=120, top=5)

#  Не знаю, почему, но сразу все три поисковика bm25, bm15, bm11 не
#  получается запустить за один запуск программы, нужно по очереди
#  Я взяла только 12000 запросов из-за ошибки памяти :с
