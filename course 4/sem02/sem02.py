from sklearn.feature_extraction.text import TfidfVectorizer
from math import log10
import numpy as np
import pandas as pd
import csv
import os
import pymorphy2
import re

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
            print('wait...')
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
        bm25_matrix = np.zeros(self.matrix.shape)
        n = [sum([1 for doc in self.docs if word in doc]) for word in
             self.dictionary]
        for idxw, word in enumerate(self.dictionary):
            for idxd, doc in enumerate(self.docs):
                bm25_matrix[idxd, idxw] = self.bm25(
                    doc, [word], [n[idxw]], len(doc))
            if int(((idxw / len(self.dictionary)) * 100) % 10) == 0:
                print(f'{int(idxw / len(self.dictionary) * 100)}%')
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

    def search_iter(self, query, top=5):
        query = [w.strip(r',\.\"!–?-\'\"\(\)\"-::—;)(\«\»\W')
                 for w in query.split()]
        query = [pmm.normal_forms(word)[0] for word in query]
        n = [sum([1 for doc in self.docs if word in doc]) for word in query]
        res = []
        texts = []
        for i, d in enumerate(self.docs):
            score = self.bm25(d, query, n, len(d))
            if score > 0.0 and self.data['question'][i] not in texts:
                res.append([i, score, self.data['question'][i]])
                texts.append(self.data['question'][i])
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

    def test_time(self):
        test_data = pd.read_csv('quora_question_pairs_rus.csv')[:self.top]
        answers = list(test_data['is_duplicate'])
        queries = [[i, j] for i, j in
                   enumerate(test_data['question1']) if answers[i] == 1]
        for idx, q1 in enumerate(queries):
            res_iter = [x[0] for x in bm25.search_iter(q1[1], top=15)]
            res_matrix = [x[0] for x in bm25.search_matrix(q1[1], top=15)]
            print(idx, q1[0], q1[1], test_data['question2'][q1[0]])
            # print('results', res_iter, res_matrix)
            accuracy_iter = 1 if q1[0] in res_iter else 0
            accuracy_matrix = 1 if q1[0] in res_matrix else 0
            print(accuracy_iter, accuracy_matrix)
            print('=================')
        return


if __name__ == '__main__':
    bm25 = BM25(top=10000)
    bm25.test_time()
    # print(bm25.search_iter('как я могу быть хорошим геологом?', 6))
    # bm25.search_matrix('каникулы', 10)
