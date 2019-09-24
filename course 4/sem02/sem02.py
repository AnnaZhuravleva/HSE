from sklearn.feature_extraction.text import TfidfVectorizer
from math import log10
import numpy as np
import pandas as pd
import csv
import pymorphy2


pmm = pymorphy2.MorphAnalyzer()
vectorizer = TfidfVectorizer()

k = 2.0
b = 0.75


data = pd.read_csv('collection.csv')
collection = len(data['question2'])
docs = [str(doc).split(' ') for doc in data['question2']]
avg = np.mean([len(doc) for doc in docs]).round(5)


def normalize():
    data0 = pd.read_csv('quora_question_pairs_rus.csv')
    with open('collection.csv', 'w', newline='', encoding='utf8') as w:
        writer = csv.writer(w, delimiter=',')
        writer.writerow(['question', 'question2'])
        for idx, doc in enumerate(docs):
            words = [w.strip(r',\.\"!–?-\'\"\(\)\"-::—;)(\«\»\W') for w in doc]
            words = [pmm.normal_forms(word)[0] for word in words]
            writer.writerow([data0['question2'][idx], ' '.join(words)])


def bm25(doc, query, n, ld) -> float:
    score = 0.0
    for number, word in enumerate(query):
        idf = log10((collection - n[number] + 0.5) / (n[number] + 0.5))
        tf = doc.count(word)/ld
        score += idf * (tf * (k + 1.0)) / (tf + k * (1 - b + (b * ld/avg)))
    return round(score, 5)


def search(query):
    print(f"Осуществляем поиск по запросу {query}")
    query = query.split()
    query = [pmm.normal_forms(word)[0] for word in query]
    n = [sum([1 for doc in docs if word in doc]) for word in query]
    res = []
    for i, d in enumerate(docs):
        tmp = bm25(d, query, n, len(d))
        if tmp > 0.0:
            res.append([tmp, i, d, data['question'][i]])
    res = sorted(res, key=lambda x: x[0], reverse=True)
    print("Вот 25 наиболее подходящих документов")
    print("\n".join(
        [f'text id:{x[1]}, bm25: {x[0]}, text: {x[3]}' for x in res[:25]]))


def tf_idf_matrix():
    return vectorizer.fit_transform(data['question2'])


if __name__ == '__main__':
    search('рождественские каникулы')
    pass
