# -*- coding: utf-8 -*-
# %load_ext autoreload

import time
import gensim
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
# from elmo_helpers import tokenize, get_elmo_vectors, load_elmo_embeddings
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from BM25 import Data, BM25
from scipy import spatial
# import tensorflow as tf
from time import time
import urllib.request
import pandas as pd
import numpy as np
import collections
import pymorphy2
import logging
import nltk
import sys
import csv
import re
import os


pmm = pymorphy2.MorphAnalyzer()
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
root.addHandler(handler)
nltk.download('punkt')


class DataSet:

  def __init__(self, corpus):
    self.corpus = pd.read_csv(corpus)
    self.collection = self.corpus['question2']

  def simple_preproc(self, query):
      return [pmm.normal_forms(word)[0] for word in nltk.word_tokenize(query)]

  def normalized_collection(self):
      a = 0
      with open('collection.csv', 'w', newline='', encoding='utf8') as w:
          writer = csv.writer(w, delimiter=',')
          writer.writerow(['question1', 'question2', 'is_duplicate',
                           'question1_n', 'question2_n',])
          for j, x, z in zip(self.corpus['question1'],
                             self.corpus['question2'],
                             self.corpus['is_duplicate']):
              try:
                  line1 = self.simple_preproc(j)
                  line1 = ' '.join(line1)
              except TypeError:
                  line1 = ' '
              try:
                  line2 = self.simple_preproc(x)
                  line2 = ' '.join(line2)
              except TypeError:
                  line2 = ' '
              writer.writerow([j, x, z, line1, line2])
              print(a)
              a += 1
      


class FastTextSearch(DataSet):

    def __init__(self, model, corpus):
        logging.info('====\nStart FastText initializing!')
        DataSet.__init__(self, corpus=corpus)
        self.model = gensim.models.KeyedVectors.load(model)
        self.test_data = []
        if os.path.isfile('models/fasttext.npy'):
            self.matrix = np.load('models/fasttext.npy')
        else:
            self.matrix = self.index_fasttext()
        logging.info('FastText initialized!')
        
    def build_vec(self, query):
        if isinstance(query, str):
            query = self.simple_preproc(query)
        lemmas_vectors = np.zeros((len(query), self.model.vector_size))
        vec = np.zeros((self.model.vector_size,))
        for idx, lemma in enumerate(query):
            if lemma in self.model.vocab:
                lemmas_vectors[idx] = self.model.wv[lemma]
            else:
                pass
        if lemmas_vectors.shape[0] is not 0:
            vec = np.mean(lemmas_vectors, axis=0)
        return vec

    def fit(self):
        logging.info('Wait: indexing of fasttext')
        matrix_fasttext = np.zeros((len(self.collection), self.model.vector_size))
        start_time = time()
        for row, query in enumerate(self.collection):
            vector = self.build_vec(query.split()) # наш корпус уже нормализован
            for idx, cell in enumerate(vector):
                matrix_fasttext[row][idx] = cell
        logging.info(f'Indexing FastTextSearch takes {time() - start_time} sec')
        if not os.path.isdir(os.path.join(os.path.abspath, 'models')):
            os.mkdir('models')
        np.save('models/fasttext.npy', matrix_fasttext)
        return matrix_fasttext

    def build_test_data(self):
        logging.info('Building Test Data')
        if os.path.isfile('data/test_data_fasttext.npy'):
            test_data = np.load('data/test_data_fasttext.npy', allow_pickle=True)
        else:
            test_data = collections.defaultdict()
            for idx, question in enumerate(self.corpus['question1_n']):
              if self.corpus['is_duplicate'][idx] == 1:
                test_data[idx] = self.build_vec(question)
            np.save('data/test_data_fasttext.npy', test_data)
        logging.info('Test Data ready!')
        return test_data

    def measure_accuracy(self, corpus_size=200):
        accuracy = 0
        for idx, query in enumerate(self.corpus['question1_n'][:corpus_size]):
            res = [x[0] for x in self.search(query)]
            accuracy += int(idx in res) 
        return accuracy / corpus_size

    def search(self, query):
        vec = self.build_vec(query)
        res = cosine_similarity([vec], self.matrix)
        docs = [(idx, doc) for idx, doc in enumerate(res[0])]
        docs = sorted(docs, key=lambda x: x[1], reverse=True)
        docs = [(x[0], x[1], self.corpus['question2'][x[0]]) for x in docs[:5]]
        return docs


if __name__ == '__main__':
  corpus = 'data/collection.csv'
  model = 'fasttext/model.model'
  fts = FastTextSearch(model=model, corpus=corpus)
  print(fts.search('зарплата Индии'))
  print(fts.measure_accuracy())
  
