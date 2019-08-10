#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import log10
import random
import re
import string
import sys


class Scorer:
    def __init__(self, ngramsvocabulary):
        with open(ngramsvocabulary, 'r', encoding='utf-8') as f:
            self.ngrams = {}
            total = 0
            for line in f.readlines():
                self.ngrams[line.split(' ')[0]] = int(line.split(' ')[1])
                total += int(line.split(' ')[1])
            for key in self.ngrams:
                self.ngrams[key] = log10(float(self.ngrams[key]) / total)

    def score(self, text):
        self.text = (re.sub(r'[\W\d]', '', text)).upper()

        def text_bigrams(text):
            for i in range(len(text)):
                yield text[i:i + 2]

        def score(text, ngrams):
            return sum([self.ngrams[i] for i in text if i in self.ngrams])

        return score(list(text_bigrams(self.text)), self.ngrams)

    def __call__(self, *kwargs):
        return self.score(*kwargs)


class Decoder:
    def __init__(self, score_func, encryptionkey):
        self.alphabet = string.ascii_uppercase
        self.encryption_ = encryptionkey
        self.encr = {k: v for v, k in zip(self.encryption_, self.alphabet)}
        decr = {self.encr[k]: k for k in self.encr}
        decr = sorted(decr.items(), key=lambda decr: decr[0])
        decr = {i[0]: i[1] for i in decr}
        self.decr = decr
        self.decryption_ = ''.join([str(i) for i in decr.values()])
        self.scorer = score_func

    def fit(self, ciphertext, num_trials):
        key = list(self.encryption_)
        dict = {}

        def set_decr(key):
            encr = {k: v for v, k in zip(key, list(self.alphabet))}
            decr = {encr[k]: k for k in encr}
            decr = sorted(decr.items(), key=lambda decr: decr[0])
            decr = {i[0]: i[1] for i in decr}
            return decr

        def local_trans(ciphertext, localdecr):
            plaintext = ''
            for i in range(len(ciphertext)):
                let = ciphertext[i]
                if let in localdecr:
                    plaintext += str(localdecr[let])
                else:
                    plaintext += str(let)
            return plaintext
        for i in range(num_trials):
            decr = set_decr(key)
            text_to_score = local_trans(ciphertext, decr)
            score = self.scorer(text_to_score)
            dict[score] = ''.join([i for i in key])
            random.shuffle(key)

        best_score = max(dict.keys())
        best_key = dict[best_score]
        self.encr = {k: v for v, k in zip(best_key, list(self.alphabet))}
        self.decr = set_decr(best_key)
        self.decryption_ = ''.join([i for i in self.decr.values()])
        self.encryption_ = best_key
        return self

    def transform(self, ciphertext):
        plaintext = ''
        for i in range(len(ciphertext)):
            let = ciphertext[i]
            if let in self.decr:
                plaintext += str(self.decr[let])
            else:
                plaintext += str(let)
        return plaintext

    def inverse_transform(self, plaintext):
        ciphertext = ''
        for i in range(len(plaintext)):
            let = plaintext[i]
            if l in self.encr:
                ciphertext += str(self.encr[let])
            else:
                ciphertext += str(let)
        return ciphertext


if __name__ == '__main__':
    source = r'english_bigrams.txt'
    letters = list(string.ascii_uppercase)
    # l = list(('zklyqpnifjdcutvwsxmagoebhr').upper())  # Here is an initial
    # Caesar cipher
    # ptext = 'THE MAN WHO DOES NOT READ BOOKS HAS NO ADVANTAGE
    # OVER THE MAN THAT CAN NOT READ THEM. --MARK TWAIN'
    # ctext = 'AIQ UZT EIV YVQM TVA XQZY KVVDM IZM TV ZYOZTAZNQ VOQX AIQ
    # UZT AIZA LZT TVA XQZY AIQU. --UZXD AEZFT'
    num_trials = 10
    ptext = sys.stdin.readline()
    ctext = sys.stdin.read()
    scorer = Scorer(source)
    decoder = Decoder(scorer, letters)
    decoder = decoder.fit(ctext, num_trials)
    plaintext = decoder.transform(ctext)
    ciphertext = decoder.inverse_transform(ptext)
