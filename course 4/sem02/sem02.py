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
        self.data = pd.read_csv('collection.csv')
        self.collection = self.data['question2'][:top]
        self._length = len(self.collection)
        self.docs = [str(doc).split(' ') for doc in self.collection]
        self.avg = np.mean([len(doc) for doc in self.docs]).round(5)
        self.vectorizer = TfidfVectorizer()
        self.model = self.vectorizer.fit(self.collection)
        self.matrix = self.vectorizer.transform(self.collection)
        self.dictionary = self.vectorizer.get_feature_names()
        name = re.sub(r'\.', '', f'bm25_matrix_b{self.b}') + '.npy'
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
        return round(score, 8)

    def bm25_build_matrix(self, name):
        bm25_matrix = np.zeros(self.matrix.shape)
        n = [sum([1 for doc in self.docs if word in doc]) for word in
             self.dictionary]
        for idxw, word in enumerate(self.dictionary):
            for idxd, doc in enumerate(self.docs):
                bm25_matrix[idxd, idxw] = self.bm25(
                    doc, [word], [n[idxw]], len(doc))
            if ((idxw / len(self.dictionary)) * 100) % 10 == 0:
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

    def testing(self):
        test_data = pd.read_csv('quora_question_pairs_rus.csv')
        answers = list(test_data['is_duplicate'])
        queries = [j for i, j in
                   enumerate(test_data['question1']) if answers[i] == 1]
        questions1 = test_data['question1']
        questions2 = test_data['question2']
        for q1 in queries[:2]:
            res_iter = [x[0] for x in bm25.search_iter(q1, top=5)]
            res_matrix = [x[0] for x in bm25.search_matrix(q1, top=5)]
            print('results', res_iter, res_matrix)
            accuracy_iter = [[q1, questions1[item], questions2[item],
                              answers[item]] for item in res_iter]
            accuracy_matrix = [[q1, questions1[item], questions2[item],
                                answers[item]] for item in res_matrix]
            print(accuracy_iter)
            print(accuracy_matrix)
            print('=================')
        return


if __name__ == '__main__':
    bm25_440000 = BM25(top=440000)
    bm25_440000.search_iter('каникулы', 10)
    bm25 = BM25()
    bm25.testing()
   # bm25.search_matrix('каникулы', 10)
