# python3
# coding: utf-8

import gensim
from gensim.models import Word2Vec, KeyedVectors
import zipfile
import urllib.request
import numpy as np
import pandas as pd
import nltk
import pymorphy2
from scipy import spatial
import time
import tensorflow as tf
from elmo_helpers import tokenize, get_elmo_vectors, load_elmo_embeddings

pmm = pymorphy2.MorphAnalyzer()
nltk.download('punkt')


class FastTextSearch:

    def __init__(self):
        self.model = gensim.models.KeyedVectors.load('fasttext/model.model')
        self.collection = pd.read_csv('data/collection.csv') # возьмем тот же файл, что и в прошлой домашке
        self.corpus = self.collection['question2']
        self.questions = pd.read_csv('data/quora_question_pairs_rus.csv')['question1']
        self.test_corpus = self.test_data()
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
        matrix_fasttext = np.zeros((corpus.shape[0], self.model.vector_size))
        start_time = time.time()
        for row, query in enumerate(self.corpus):  
          vector = self.fasttext_search(query.split())
          for idx, cell in enumerate(vector):
              matrix_fasttext[row][idx] = cell
        print(time.time() - start.time)
        return matrix_fasttext

    def test_data(self):
        test_data = []
        for question in self.questions[:3]:
            question = [pmm.normal_forms(word)[0] for word in nltk.word_tokenize(question)]
            vector = self.fasttext_search(query.split(), fasttext_model)
            test_data.append(vector)
        return test_data

    def testing(self):
        vec = self.test_corpus[0]
        res = {}
        for i in range(2000):
          row = self.matrix[i]
          cos_sim = spatial.distance.cosine(row, vec)
          res[i] = cos_sim

        res = sorted(res.items(), key=lambda x: x[1], reverse=True)[:5]
        print(res)
        return res


class ElmoSearch:

    def __init__(self):
        ops.reset_default_graph()
        self.elmo_path = 'elmo'
        self.batcher, self.sentence_character_ids, \
                      self.elmo_sentence_input = load_elmo_embeddings(self.elmo_path)

    def FitElmo(self, sentences):
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            start = time.time()
            elmo_vectors = get_elmo_vectors(
                sess, sentences, self.batcher,\
                self.sentence_character_ids, self.elmo_sentence_input)
            print(time.time() - start)
        return elmo_vectors
        
        
elmo_path = 'elmo'

raw_sentences = [
    'хочу изучить технику стрельбы из лука',
    'можешь нарезать мелко лук, возьми для этого большой нож']

sentences = [tokenize(s) for s in raw_sentences]

# Я не знаю, верно ли я все написала, т.к. глупая и не могу справиться с установкой elmo и tensorflow
        
if __name__ == '__main__':
    fasttext = FastTextSearch()
    fasttext.testing()



  



