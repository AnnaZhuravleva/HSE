# -*- coding: utf-8 -*-
# %load_ext autoreload

from elmo_helpers import tokenize, get_elmo_vectors, load_elmo_embeddings
from gensim.models import Word2Vec, KeyedVectors
from BM25 import Data, BM25
from scipy import spatial
import tensorflow as tf
from time import time
import urllib.request
import pandas as pd
import numpy as np
import collections
import pymorphy2
import logging
import sklearn
import zipfile
import gensim
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


def build_test_data(corpus, collection):
  data = pd.read_csv(corpus)
  collection = pd.read_csv(collection)['question2']
  top = len(data['question1'])
  test_data = []
  for idx in range(top):
    if data['is_duplicate'][idx] == 1:
      test_data.append((idx, data['question1'][idx], collection[idx]))
  return test_data

class DataSet:

  def __init__(self, collection, corpus):
    self.collection = pd.read_csv(collection)['question2']
    self.corpus = pd.read_csv(corpus)
    # self.test_corpus = self.build_test_corpus()

  def simple_preproc(self, query):
    return [pmm.normal_forms(word)[0] for word in nltk.word_tokenize(query)]

  def build_test_corpus(self):
    data = collections.defaultdict()
    
    for i, j in list(enumerate(self.corpus['question1'])):
      if self.corpus['is_duplicate'][i] == 1:
        query = self.simple_preproc(j)
        data[i] = query
    
    return data

  def normalized_collection(self):
    a = 0
    with open('normcollection.csv', 'w', newline='', encoding='utf8') as w:
      writer = csv.writer(w, delimiter=',')
      writer.writerow(['question1', 'question2', 'is_duplicate'])
      for i,j,z in zip(self.collection, self.corpus['question1'], self.corpus['is_duplicate']):
        line = ' '.join(self.simple_preproc(j))
        writer.writerow([line,  i, z])
        print(a)
        a += 1


class FastTextSearch(DataSet):

    def __init__(self, model, collection, corpus):
      logging.info('====\nStart FastText initializing!')
      DataSet.__init__(self, collection=collection, corpus=corpus)
      self.model = gensim.models.KeyedVectors.load(model)
      self.test_data = self.build_test_data()
      if os.path.isfile('fasttext.npy'):
        self.matrix = np.load('modesl/fasttext.npy')
      else:
        self.matrix = self.index_fasttext()
      logging.info('FastText initialized!')
        
    def fasttext_search(self, query):

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

    def index_fasttext(self):
      logging.info('Wait: indexing of fasttext')
      matrix_fasttext = np.zeros((len(self.collection), self.model.vector_size))
      start_time = time()
      for row, query in enumerate(self.collection):
        vector = self.fasttext_search(query.split()) # наш корпус уже нормализован
        for idx, cell in enumerate(vector):
            matrix_fasttext[row][idx] = cell
      logging.info(f'Indexing FastTextSearch takes {time() - start_time} sec')
      if not os.path.isdir(os.path.join(os.path.abspath, 'models')):
        os.mkdir('models')
      np.save('models/fasttext.npy', matrix_fasttext)
      return matrix_fasttext

    def build_test_data(self):
      test_data = collections.defaultdict()
      for idx, question in self.test_corpus.items():
        test_data[idx] = self.fasttext_search(question)
      return test_data

    def measure_accuracy(self, corpus_size=200):
      accuracy = 0
      queries = list(self.test_data.items())[:100]
      for vec in enumerate(queries):
        res = collections.defaultdict()
        for idx, row in self.matrix:
          res[idx] = spatial.distance.cosine(row, vec[0])
        res = sorted(res.items(), key=lambda x: x[1], reverse=True)
        accuracy += int(queries[vec] in list(res.keys())[:5])
        return accuracy / 100


class ElmoSearch:
  
  def __init__(self):
    tf.reset_default_graph()
    self.batcher, self.sentence_character_ids, self.elmo_sentence_input = \
    load_elmo_embeddings(elmo_path)
    self.vectors = []
    self.collection = []
    
  def build_vec(self, sentences):
     with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        elmo_vectors = get_elmo_vectors(
            sess, sentences, self.batcher, self.sentence_character_ids,
            self.elmo_sentence_input)
        
        results = []
        for vect, sent in zip(elmo_vectors, sentences):
          results.append(np.mean(vect[:len(sent), :], axis=0))
        
        return results
    
  def indexing(self, sentences):
    self.collection = sentences
    with tf.Session() as sess:
      sess.run(tf.global_variables_initializer())
      start = time()
      sentences = [tokenize(sent) for sent in sentences]
      for sent in sentences:
        sent_vec = self.build_vec([sent])
        self.vectors.append(sent_vec[0])
        
      logging.info(f'=====\n'\
            f'ElmoSearch Indexing takes {time() - start} sec'\
            f'for {len(sentences)} docs')
      return self.vectors
    
  def elmo_search(self, query):
    query = self.simple_preproc(query)
    query_vec = self.build_vec([query])
    results = []
    for idx, doc in enumerate(self.collection):
      results.append((idx, spatial.distance.cosine(self.vectors[idx], query_vec), doc))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    
    return results
  
  def measure_accuracy(self, test_data, number=100, top=5):
    queries = test_data[:number]
    accuracy = 0
    for q1 in queries:
      res = [x[0] for x in self.elmo_search(q1[1])[:top]]
      accuracy += int(q1[0] in res)
    accuracy = "{:.0%}".format(accuracy / number)
    return accuracy


class Models(BM25, FastTextSearch, ElmoSearch):

  def __init__(self, elmo_path, collection, fasttext_model, corpus):
    self.collection = pd.read_csv(collection)
    self.corpus_path = corpus
    # self.elmosearch = ElmoSearch()
    self.fasttext = FastTextSearch(fasttext_model, corpus=corpus, collection=collection)
    # self.bm25 = BM25()

  def fit_elmo(self):
    data = pd.read_csv(self.collection['question2'])
    vectors = self.elmosearch.indexing(data)
    np.save('elmo_vectors.npy', np.array(vectors)) 
    return

  def fit_all(self):
    self.fit_fasttext()
    self.fit_elmo()
    return


if __name__ == '__main__':
  elmo_path = 'elmo'
  collection = 'data/collection.csv'
  model = 'fasttext/model.model'
  corpus = 'data/quora_question_pairs_rus.csv'
  # test_data = build_test_data(corpus, collection)
  # fts = FastTextSearch(model=model, corpus=corpus, collection=collection, test_corpus=test_data)
  # fts.measure_accuracy()
  # els = ElmoSearch()
  # els.indexing(pd.read_csv(collection)['question2'][:200])
  # elmo_accuracy = els.measure_accuracy(test_data=test_data,number=100)
  # models = Models(elmo_path, collection, model, corpus)
  ds = DataSet(collection, corpus)
  ds.normalized_collection()
  # print(models.fasttext.fasttext_search('я дебил'))
  
