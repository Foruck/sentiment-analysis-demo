# -*- coding:utf-8 -*-

import os
import xml.dom.minidom
import re
import h5py

cn_corpus, en_corpus = [], []
cn_sen, en_sen = [], []
direp = {'CN':"cn_sample_data", 'EN':"en_sample_data"}
filep = {'raw_POS':"sample.positive.xml", 'raw_NEG':"sample.negative.xml", 'POS':"pure_sample.positive.xml", 'NEG':"pure_sample.nagative.xml"}


def preprocess_string(s, tag):
    if s[-1] == '\n':
        s = s[:-1]
    s = s.replace('\t', '')
    if "<review" not in s and "<reviews>" not in s and "</review>" not in s and "</reviews>" not in s:
        s = s.replace('&lt;', '《')
        s = s.replace('&gt;', '》')
    if tag == "CN":
        s.replace('<<', '《')
        s.replace('>>', '》')
    return re.sub(r'&(?!(lt;)|(gt;)|(amp;)|(apos;)|(quot;))', '&amp;', s)

def preprocess_file(lang, tag):
    fname = os.path.join(direp[lang], filep['raw_' + tag])
    with open(fname, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()
        lines = list(filter(lambda x:x != '\n', lines))
        for i in range(len(lines)):
            lines[i] = preprocess_string(lines[i], tag)
    
    fname = os.path.join(direp[lang], filep[tag])
    with open(fname, 'w', encoding='utf-8') as f_out:
        for line in lines:
            f_out.write(line + '\n')

preprocess_file('CN', 'POS')
fname = os.path.join(direp['CN'], filep['POS'])
dom = xml.dom.minidom.parse(fname)
collection = dom.documentElement
reviews = collection.getElementsByTagName("review")
for i in range(len(reviews)):
    s = reviews[i].firstChild.data.strip()
    cn_corpus.append(s)
    cn_sen.append(1)

preprocess_file('CN', 'NEG')
fname = os.path.join(direp['CN'], filep['NEG'])
dom = xml.dom.minidom.parse(fname)
collection = dom.documentElement
reviews = collection.getElementsByTagName("review")
for i in range(len(reviews)):
    s = reviews[i].firstChild.data.strip()
    cn_corpus.append(s)
    cn_sen.append(-1)

preprocess_file('EN', 'POS')
fname = os.path.join(direp['EN'], filep['POS'])
dom = xml.dom.minidom.parse(fname)
collection = dom.documentElement
reviews = collection.getElementsByTagName("review")
for i in range(len(reviews)):
    s = reviews[i].firstChild.data.strip()
    en_corpus.append(s)
    en_sen.append(1)

preprocess_file('EN', 'NEG')
fname = os.path.join(direp['EN'], filep['NEG'])
dom = xml.dom.minidom.parse(fname)
collection = dom.documentElement
reviews = collection.getElementsByTagName("review")
for i in range(len(reviews)):
    s = reviews[i].firstChild.data.strip()
    en_corpus.append(s)
    en_sen.append(-1)

f1 = h5py.File('cn_basic.h5', 'w')
f1['sentence'] = cn_corpus
f1['polarity'] = cn_sen
f1.close()

f2 = h5py.File('en_basic.h5', 'w')
f2['sentence'] = en_corpus
f2['polarity'] = en_sen
f2.close()