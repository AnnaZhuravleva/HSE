from sklearn.feature_extraction.text import TfidfVectorizer
from math import log10
import numpy as np
import pandas as pd
import csv
import os
import pymorphy2
import re
import time

pmm = pymorphy2.MorphAnalyzer()


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
        print('wait...')
        bm25_matrix = np.zeros(self.matrix.shape)
        n = [sum([1 for doc in self.docs if word in doc]) for word in
             self.dictionary]
        for idw, word in enumerate(self.dictionary):
            for idd, doc in enumerate(self.docs):
                bm25_matrix[idd, idw] = self.bm25(
                    doc, [word], [n[idw]], len(doc))
            # if int(((idw / len(self.dictionary)) * 100) % 10) == 0:
            #   print(f'{int(idw / len(self.dictionary) * 100)}%')
        np.save(name, bm25_matrix)
        print('matrix saved')
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
        print(f'Сравним время работы двух поисковиков на {number} запросах')
        start_iter = time.time()
        for item in self.queries[:number]:
            self.search_iter(item[1])
        end_iter = time.time()
        print(f'Время работы первого поисковика - {end_iter - start_iter}')
        start_matrix = time.time()
        for item in self.queries[:number]:
            self.search_matrix(item[1])
        end_matrix = time.time()
        print(f'Время работы второго поисковика - {end_matrix - start_matrix}')
        return [end_iter - start_iter, end_matrix - start_matrix]

    def test_query(self, query='рождественские каникулы', top=10):
        print(f'Выводим результаты по запросу {query}')
        print('Первый поисковик')
        for i, j in enumerate(self.search_iter(query, top)):
            text = self.test_data['question2'][j[0]]
            print(f'{i}.\tText_id: {j[0]},\tscore: {j[1]},\ttext: {text}')
        print('Второй поисковик')
        for i, j in enumerate(self.search_matrix(query, top)):
            text = self.test_data['question2'][j[0]]
            print(f'{i}.\tText_id: {j[0]},\tscore: {j[1][0]},\ttext: {text}')
        return

    def test_accuracy(self, number=1000, top=5):
        print(f'Сравним точность двух поисковиков на {number} запросах'
              f'при b = {self.b}')
        queries = self.queries[:number]
        accuracy_iter = 0
        accuracy_matrix = 0
        for q1 in queries:
            res_iter = [x[0] for x in self.search_iter(query=q1[1], top=top)]
            accuracy_iter += int(q1[0] in res_iter)
        print(f'Точность первого поисковика - ' +
              "{:.0%}".format(accuracy_iter / number))
        for q1 in queries:
            res_matrix = [x[0] for x in self.search_iter(query=q1[1], top=top)]
            accuracy_matrix += int(q1[0] in res_matrix)
        print('Точность второго поисковика - ' +
              "{:.0%}".format(accuracy_matrix / number))

        return [accuracy_iter / number, accuracy_matrix / number]


if __name__ == '__main__':
    bm25 = BM25(top=10000)  # В скобках указываем количество документов
    bm25.test_time(10)  # В скобках указываем количество запросов
    bm25.test_query('зарплата врача в Индии', top=10)  # В скобках указываем
    # количество результатов
    bm25.test_accuracy(number=10, top=5)
    # bm15 = BM25(b=0, top=10000)
    # bm11 = BM25(b=1, top=10000)
