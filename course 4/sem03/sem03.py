# -*- coding: utf-8 -*-
# %load_ext autoreload

from gensim.models import Word2Vec, KeyedVectors
import gensim
import zipfile
import urllib.request
import numpy as np
import pandas as pd
import nltk
import pymorphy2
from scipy import spatial
import re
import os
import tensorflow as tf
import sys
import time
from time import time
from elmo_helpers import tokenize, get_elmo_vectors, load_elmo_embeddings
from sem02 import Data, BM25

pmm = pymorphy2.MorphAnalyzer()
nltk.download('punkt')


def build_test_data(corpus, collection):
  data = pd.read_csv(corpus)
  collection = pd.read_csv(collection)
  top = len(data['question1'])
  test_data = []
  for idx in range(top):
    if data['is_duplicate'][idx] == 1:
      test_data.append((idx, data['question1'][idx], collection['question2'][idx]))
  return test_data

class FastTextSearch:

    def __init__(self, model, collection, corpus, test_corpus):
        self.model = gensim.models.KeyedVectors.load(model)
        self.collection = pd.read_csv(collection) # возьмем тот же файл, что и в прошлой домашке
        self.corpus = self.collection['question2']
        self.questions = pd.read_csv(corpus)['question1']
        self.test_corpus = self.test_data(test_corpus)
        self.matrix = self.index_fasttext()
        
    def fasttext_search(self, query):

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
        matrix_fasttext = np.zeros((self.corpus.shape[0], self.model.vector_size))
        start_time = time()
        for row, query in enumerate(self.corpus):  
          vector = self.fasttext_search(query.split()) # наш корпус уже нормализован
          for idx, cell in enumerate(vector):
              matrix_fasttext[row][idx] = cell
        print(f'Indexing FastTextSearch takes {time() - start_time} sec')
        return matrix_fasttext

    def simple_preproc(self, query):
        return [pmm.normal_forms(word)[0] for word in nltk.word_tokenize(query)]
        
     def test_data(self, test_corpus):
        test_data = {}
        for question in test_corpus[:100]:
            query = self.simple_preproc(question[1])
            vector = self.fasttext_search(query)
            test_data[question[0]] = vector
        return test_data

    def measure_accuracy(self, corpus_size=200):
        accuracy = 0
        corpus = self.test_corpus
        for q1 in corpus:
          try:
            vec = self.test_corpus[q1]
            res = {}
            for i in range(corpus_size):
              row = self.matrix[q1]
              cos_sim = spatial.distance.cosine(row, vec)
              res[i] = cos_sim
            res = sorted(res.items(), key=lambda x: x[1], reverse=True)[:5]
            accuracy += int(q1 in [x[0] for x in res])
          except:
            pass

        return accuracy /100


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
        
      print(f'=====\n'\
            f'ElmoSearch Indexing takes {time() - start} sec'\
            f'for {len(sentences)} docs')
      return self.vectors
    
  def simple_preproc(self, query):
      return [pmm.normal_forms(word)[0] for word in nltk.word_tokenize(query)]
    
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


if __name__ == '__main__':
  elmo_path = 'elmo'
  collection = 'collection.csv'
  model = 'fasttext/model.model'
  corpus = 'quora_question_pairs_rus.csv'
  test_data = build_test_data(corpus, collection)
  fts = FastTextSearch(model=model, corpus=corpus, collection=collection, test_corpus=test_data)
  fts.measure_accuracy()
  els = ElmoSearch()
  els.indexing(pd.read_csv(collection)['question2'][:200])
  elmo_accuracy = els.measure_accuracy(test_data=test_data,number=100)
  bm25 = BM25(top=12000)
  bm25.test_accuracy(number=100)
  
