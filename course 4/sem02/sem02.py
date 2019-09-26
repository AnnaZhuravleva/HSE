from sklearn.feature_extraction.text import TfidfVectorizer
from math import log10
import numpy as np
import pandas as pd
import csv
import pymorphy2


pmm = pymorphy2.MorphAnalyzer()

k = 2.0
b = 0.75

class BM25:

    def __init__(self):
        self.data = pd.read_csv('collection.csv')
        self.collection = self.data['question2']
        self._length = len(self.data['question2'])
        self.vectorizer = TfidfVectorizer()
        self.docs = [str(doc).split(' ') for doc in self.data['question2']]
        self.avg = np.mean([len(doc) for doc in self.docs]).round(5)
        self.model = self.vectorizer.fit(self.collection)
        self.matrix = self.vectorizer.transform(self.collection)

    def bm25(self, doc, query, n, ld):
        score = 0.0
        for number, word in enumerate(query):
            idf = log10((self._length - n[number] + 0.5) / (n[number] + 0.5))
            tf = doc.count(word)/ld
            score += idf * (tf * (k + 1.0)) / (tf + k * (1 - b + (b * ld/self.avg)))
        return round(score, 5)

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
        print(res[:5])

    def normalize(self):
        data0 = pd.read_csv('quora_question_pairs_rus.csv')
        with open('collection.csv', 'w', newline='', encoding='utf8') as w:
            writer = csv.writer(w, delimiter=',')
            writer.writerow(['question', 'question2'])
            for idx, doc in enumerate(self.docs):
                words = [w.strip(r',\.\"!–?-\'\"\(\)\"-::—;)(\«\»\W') for w in doc]
                words = [pmm.normal_forms(word)[0] for word in words]
                writer.writerow([data0['question2'][idx], ' '.join(words)])


if __name__ == '__main__':
   bm25 = BM25()
   bm25.search_iter('рождественские каникулы')
