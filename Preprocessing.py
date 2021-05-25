#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import psycopg2
import numpy as np
import sys
import csv
import re
import string
from nltk import word_tokenize
from collections import Counter
from itertools import chain
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import swifter

path_data = 'C:/Users/Zukkiii_/Youtube Comments Mining/Data/'
path_resource = 'C:/Users/Zukkiii_/Youtube Comments Mining/Resource/'

fSlang = path_resource + 'word_formalization_dic.txt'
sw = open(fSlang, encoding='UTF-8', errors='ignore', mode='r'); SlangS=sw.readlines(); sw.close()
SlangS = {slang.strip().split(':')[0]:slang.strip().split(':')[1] for slang in SlangS}

factory = StemmerFactory()
stemmer = factory.create_stemmer()

stoplist = []
stoplist_file = open(path_resource + 'stoplist.txt', 'r', encoding="UTF-8", errors='replace')
stoplist.append(stoplist_file.readlines());stoplist_file.close()
stops = set([t.strip() for t in stoplist[0]])

class preprocessing:
    def clean_text(text):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        text = text.lower() #lowecase
        text = re.sub(pattern, '', text) #remove URLs
        text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text) #remove punctuations
        #text = re.sub(r'\w*\d\w*', ' ', text) #remove words containing numbers
        text = re.sub(r'[^a-z]*([.0-9])*\d', ' ', text) #remove numbers
        text = re.sub(r'(.)\1{2,}', r'\1', text) #menghapus 2 huruf berlebih yang sama dalam 1 kata
        text = re.sub(r'[^.,a-zA-Z0-9 \n\.]','', text) #remove special characters
        text = re.sub(r'#([^\s]+)', r'\1', text) #remove hashtag
        text = re.sub('[\s]+', ' ', text) #remove additional white space
        return text
    
    def tokenize(teks):
        teks = word_tokenize(teks)
        return teks
    
    def slangword(teks):
        for i,x in enumerate(teks):
            if x in SlangS.keys():
                teks[i] = SlangS[x]
        return ' '.join(teks)
    
    def stemmed_wrapper(term):
        return stemmer.stem(term)
    
    def stopwords(teks):
        teks = [x for x in teks if x not in stops]
        return ' '.join(teks)

