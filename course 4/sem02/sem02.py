from sklearn.feature_extraction.text import TfidfVectorizer,  CountVectorizer
from math import log10
import numpy as np
import pandas as pd
import csv
import pymorphy2


pmm = pymorphy2.MorphAnalyzer()


class Data:

    def __init__(self):
        self.data = pd.read_csv('collection.csv')
        self.collection = self.data['question2'][:1000]
        self._length = len(self.collection)
        self.docs = [str(doc).split(' ') for doc in self.collection]
        self.avg = np.mean([len(doc) for doc in self.docs]).round(5)
        
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

    def __init__(self):
        super().__init__()
        self.vectorizer = TfidfVectorizer()
        self.cntvectorizer = CountVectorizer()
        self.model = self.vectorizer.fit(self.collection)
        self.cntmodel = self.cntvectorizer.fit(self.collection)
        self.matrix = self.vectorizer.transform(self.collection)

    def bm25(self, doc, query, n, ld, k=2.0, b=0.75):
        score = 0.0
        for number, word in enumerate(query):
            idf = log10((self._length - n[number] + 0.5) / (n[number] + 0.5))
            tf = doc.count(word)/ld
            score += idf * (tf * (k + 1.0)) / (tf + k * (1 - b + (b *
                                                                  ld/self.avg)))
        return round(score, 8)

    def bm25_build_matrix(self):
        bm25_matrix = np.zeros(self.matrix.shape)
        n = [sum([1 for doc in self.docs if word in doc]) for word in
             self.vectorizer.get_feature_names()]
        for idxw, word in enumerate(self.vectorizer.get_feature_names()):
            for idxd, doc in enumerate(self.docs):
                bm25_matrix[idxd, idxw] = self.bm25(
                    doc, [word], [n[idxw]], len(doc))
        np.save('bm25_matrix.npy', bm25_matrix)
        print('matrix saved')
        return bm25_matrix.shape

    def search_iter(self, query):
        query = query.split()
        query = [pmm.normal_forms(word)[0] for word in query]
        n = [sum([1 for doc in self.docs if word in doc]) for word in query]
        res = []
        texts = []
        for i, d in enumerate(self.docs):
            score = self.bm25(d, query, n, len(d))
            if score > 0.0 and self.data['question'][i] not in texts:
                res.append([score, i, self.data['question'][i]])
                texts.append(self.data['question'][i])
        res = sorted(res, key=lambda x: x[0], reverse=True)
        for t, item in enumerate(res[:5]):
            if item[0] > 0:
                print(item[1], item[0])
        return res[:25]

    def search_matrix(self, query):
        query = list(set(
            [pmm.normal_forms(word)[0] for word in query.split()]))
        matrix = np.load('bm25_matrix.npy')
        vector = np.zeros((len(self.vectorizer.get_feature_names()), 1))
        for i, j in enumerate(self.vectorizer.get_feature_names()):
            vector[i, 0] = 1 if j in query else 0
        result = matrix.dot(vector)
        res = [[i, j] for i, j in enumerate(result)]
        res = sorted(res, key=lambda x: x[1], reverse=True)
        for i, j in enumerate(res[:5]):
            print(i, j)
        return result


if __name__ == '__main__':
    bm25 = BM25()
    bm25.search_iter('правительство Индии')
    # bm25.bm25_build_matrix()
    print('==============')
    bm25.search_matrix('правительство Индии')
