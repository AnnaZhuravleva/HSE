# -*- coding: utf-8 -*-
# %load_ext autoreload

import tensorflow as tf
from configs import *
from elmo_helpers import tokenize
from elmo_helpers import get_elmo_vectors
from elmo_helpers import load_elmo_embeddings


class BM25:

    def __init__(self, k=2.0, b=0.75, top=12000):
        LOGGER.info('BM25 initializing')
        self.k = k
        self.b = b
        self.top = top
        self.data = pd.read_csv('data/collection.csv')
        self.collection = self.data['question2_n'][:top]
        self.docs = [str(doc).split(' ') for doc in self.collection]
        self.avg = np.mean([len(doc) for doc in self.docs]).round(5)
        self.vectorizer = CountVectorizer()
        self.cmatrix = self.vectorizer.fit_transform(self.collection)
        self.dictionary = self.vectorizer.get_feature_names()
        if os.path.isfile(BM25_model):
            self.matrix = np.load(BM25_model)
        else:
            self.matrix = self.fit(BM25_model)
        LOGGER.info('BM25 initialized')
    
    def simple_preproc(self, query):
        return [pmm.normal_forms(word)[0] for word in nltk.word_tokenize(query)]

    def fit(self, name):
        LOGGER.info('BM25 indexing')
        start = time()
        bm25_matrix = np.zeros(self.cmatrix.shape)
        n = [sum([1 for doc in self.docs if word in doc]) for word in
             self.dictionary]
        for idw, word in enumerate(self.dictionary):
            for idd, doc in enumerate(self.docs):
                bm25_matrix[idd, idw] = self.bm25(
                    doc, [word], [n[idw]], len(doc))
        np.save(name, bm25_matrix)
        LOGGER.info(f'BM25 indexing takes {time() - start} sec')
        return bm25_matrix

    def bm25(self, doc, query, n, ld):
        score = 0.0
        for number, word in enumerate(query):
            idf = log10((self.top - n[number] + 0.5) / (n[number] + 0.5))
            tf = doc.count(word) / ld
            score += idf * (tf * (self.k + 1.0)) / (
                    tf + self.k * (1 - self.b + (self.b * ld / self.avg)))
        return score

    def search(self, query, top=10):
        query = self.simple_preproc(query)
        vector = np.zeros((len(self.dictionary), 1))
        for i, j in enumerate(self.dictionary):
            vector[i, 0] = 1 if j in query else 0
        result = self.matrix.dot(vector)
        res = [[i, j] for i, j in enumerate(result)]
        res = sorted(res, key=lambda x: x[1], reverse=True)
        res = [(x[0], x[1], self.data['question1'][x[0]]) for x in res[:top]]
        return res


class DataSet:

    def __init__(self, corpus):
        self.corpus = pd.read_csv(corpus)
        self.collection = self.corpus['question2']

    def simple_preproc(self, query):
        return [pmm.normal_forms(word)[0] for word in nltk.word_tokenize(query)]

    def normalized_collection(self, corpuspath):
        rowcorpus = pd.read_csv(corpuspath)
        if not os.path.isdir(os.path.join(os.path.abspath, 'data')):
            os.mkdir('data')
        with open('data/collection.csv', 'w', newline='', encoding='utf8') as w:
            writer = csv.writer(w, delimiter=',')
            writer.writerow(['question1', 'question2', 'is_duplicate',
                            'question1_n', 'question2_n',])
            for j, x, z in zip(rowcorpus['question1'], \
                rowcorpus['question2'], rowcorpus['is_duplicate']):
                try:
                    line1 = ' '.join(self.simple_preproc(j))
                except TypeError:
                    line1 = ' '
                try:
                    line2 = ' '.join(self.simple_preproc(x))
                except TypeError:
                    line2 = ' '
                writer.writerow([j, x, z, line1, line2])
      

class FastTextSearch(DataSet):

    def __init__(self, model, corpus):
        LOGGER.info('FastText initializing!')
        DataSet.__init__(self, corpus=corpus)
        self.model = gensim.models.KeyedVectors.load(model)
        self.test_data = []
        self.matrix = self.fit()
        LOGGER.info('FastText initialized!')

    def fit(self):
        LOGGER.info('Wait: indexing of fasttext')
        if os.path.isfile(FastText_model):
            return np.load(FastText_model)
        matrix_fasttext = np.zeros((len(self.collection), self.model.vector_size))
        start_time = time()
        for row, query in enumerate(self.collection):
            vector = self.build_vec(query.split()) # наш корпус уже нормализован
            for idx, cell in enumerate(vector):
                matrix_fasttext[row][idx] = cell
        if not os.path.isdir(os.path.join(os.path.abspath, 'models')):
            os.mkdir('models')
        np.save(FastText_model, matrix_fasttext)
        LOGGER.info(f'Indexing FastTextSearch takes {time() - start_time} sec')
        return matrix_fasttext
        
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
        if lemmas_vectors.shape[0] != 0:
            vec = np.mean(lemmas_vectors, axis=0)
        return vec

    def search(self, query):
        vec = self.build_vec(query)
        res = cosine_similarity([vec], self.matrix)
        docs = [(idx, doc) for idx, doc in enumerate(res[0])]
        docs = sorted(docs, key=lambda x: x[1], reverse=True)
        docs = [(x[0], x[1], self.corpus['question2'][x[0]]) for x in docs[:10]]
        return docs


class ElmoSearch(DataSet):
    
    def __init__(self, corpus, elmo_path):
        LOGGER.info('Start Elmo initializing!')
        DataSet.__init__(self, corpus)
        self.elmo_path = elmo_path
        tf.reset_default_graph()
        self.batcher, self.sentence_character_ids, self.elmo_sentence_input = \
            load_elmo_embeddings(elmo_path)
        self.vectors = self.fit()
        LOGGER.info('Elmo initialized!')
    
    def fit(self, n=0):
        LOGGER.info('Wait: indexing of elmo')
        if os.path.isfile(Elmo_model):
            return np.load(Elmo_model)
        vectors = []
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            start = time()
            sentences = [tokenize(sent) for sent in self.collection[n:n+1000]]
            for idx, sent in enumerate(sentences):
                sent_vec = self.build_vec([sent])
                vectors.append(sent_vec)
                print(idx)

            LOGGER.info(f'ElmoSearch Indexing takes {time() - start} '
                        f'sec for {len(sentences)} docs')
            np.save(Elmo_model, vectors)
            return vectors
    
    def build_vec(self, sentences):
        '''
        :param: array of sentences of len >= 1
        :return: elmo vector
        '''
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            elmo_vectors = get_elmo_vectors(sess, sentences, self.batcher, self.sentence_character_ids, self.elmo_sentence_input)
            results = []
            for vect, sent in zip(elmo_vectors, sentences):
                results.append(np.mean(vect[:len(sent), :], axis=0))
            return results[0]
    
    def search_base(self, query):
        query = self.simple_preproc(query)
        vec = self.build_vec([query])
        res = cosine_similarity([vec], self.vectors)
        docs = [(idx, doc) for idx, doc in enumerate(res[0])]
        docs = sorted(docs, key=lambda x: x[1], reverse=True)
        docs = [(x[0], x[1], self.corpus['question2'][x[0]]) for x in docs[:10]]
        return docs
      
    def search(self, query):
        tf.reset_default_graph()
        batcher, sentence_character_ids, elmo_sentence_input = \
          load_elmo_embeddings(self.elmo_path)
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            elmo_vectors = get_elmo_vectors(sess, [query], batcher, sentence_character_ids, 
            elmo_sentence_input)
            results = []
            for vect, sent in zip(elmo_vectors, [query]):
                results.append(np.mean(vect[:len(sent), :], axis=0))
        vec = results
        res = cosine_similarity(vec, self.vectors)
        docs = [(idx, doc) for idx, doc in enumerate(res[0])]
        docs = sorted(docs, key=lambda x: x[1], reverse=True)
        docs = [(x[0], x[1], self.corpus['question2'][x[0]]) for x in docs[:10]]
        return docs


class TfIdfSearch(DataSet):

    def __init__(self, corpus):
        LOGGER.info('TfIdfSearch initializing!')
        DataSet.__init__(self, corpus)
        self.vectorizer = TfidfVectorizer()
        self.model = self.vectorizer.fit(self.collection)
        self.matrix = self.vectorizer.transform(self.collection)
        LOGGER.info('TfIdfSearch initialized')

    def search(self, query):
        query = self.simple_preproc(query)
        query = [' '.join(query)] if len(query) > 1 else query
        vec = self.vectorizer.transform(query)
        res = cosine_similarity(vec, self.matrix)
        docs = [(idx, doc) for idx, doc in enumerate(res[0])]
        docs = sorted(docs, key=lambda x: x[1], reverse=True)
        docs = [(x[0], x[1], self.corpus['question2'][x[0]]) for x in docs[:10]]
        return docs



class Models(BM25, FastTextSearch, ElmoSearch):

    def __init__(self, elmo_path, fasttext_model, corpus):
        self.elmosearch = 0
        self.fasttext = 0
        self.bm25 = 0
        self.tfidf = 0
        self.elmopath = elmo_path
        self.fasttextpath = fasttext_model
        self.corpuspath = corpus

    def init_elmo(self):
        self.elmosearch = ElmoSearch(self.corpuspath, self.elmopath)
        return

    def init_fasttext(self):  
        self.fasttext = FastTextSearch(self.fasttextpath, self.corpuspath)
        return
    
    def init_bm25(self):
        self.bm25 = BM25()
        return

    def init_tfidf(self):
        self.tfidf = TfIdfSearch(self.corpuspath)
        return
