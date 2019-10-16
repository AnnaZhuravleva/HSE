import time
import gensim
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from math import log10
from time import time
import pandas as pd
import numpy as np
import collections
import pymorphy2
import logging
import nltk
import sys
import csv
import os

pmm = pymorphy2.MorphAnalyzer()
nltk.download('punkt')

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
fh = logging.FileHandler("new_snake.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOGGER.addHandler(fh)

# fh = logging.StreamHandler(sys.stdout)
