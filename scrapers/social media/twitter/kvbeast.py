from sklearn.feature_extraction.text import TfidfVectorizer as kvdaddy
import hashlib as kvhash
from sklearn.externals import joblib as kvjob
import numpy as kvpie
from operator import itemgetter as kvitem
from itertools import groupby as kvgroup
import sys as kvsys

reload(kvsys)
kvsys.setdefaultencoding('utf8')

with open("processed_tweets.csv", "r") as fl:
    kv_content = fl.read().split('\n')

kv_content = [[k.replace("\"","") for k in v.split(",")] for v in kv_content]

kv_tweets = [(kv_iter[1], kv_iter[2]) for kv_iter in kv_content if len(kv_iter) > 4 and kv_iter[3].lower() =="tweet"]

kvectorizer = kvdaddy(stop_words="english")
kvectorizer.fit_transform([kv[1] for kv in kv_tweets])

kvecs = [(kv[0], kvectorizer.transform([kv[1]])[0]) for kv in kv_tweets]
words = kvectorizer.get_feature_names()
kv_namewords = []
curr_kv = kvecs[0][0]
kv_string = ''
for k in kvecs:
    if curr_kv != k[0]:
        temp_top = filter(lambda x: x[0] != k[0], kv_namewords)
        temp_top = map(lambda x: x[1:], temp_top) 
        temp_top = list(set([item for sublist in temp_top for item in sublist]))
        temp_top = sorted(temp_top, key=(lambda x: -1*x))[:5]
        temp_top = [words[t] for t in temp_top]

        kv_namewords = []
        kv_string += curr_kv + ',' + ','.join(temp_top) + '\n'
        print 'Filtered'
        print kv_string + '\n\n\n\n\n'

        curr_kv = k[0]

    kvec = k[1].T
    kvecm = [(ki, i) for i, ki in enumerate(kvec)]
    kvecm = sorted(kvecm, key=(lambda x: -1*x[0]))[:5]
    fivewords = [i[1] for i in kvecm]
    kv_namewords.append([k[0], fivewords[0], fivewords[1], fivewords[2], fivewords[3], fivewords[4]]) 
    
    print kv_string
    for v in kv_namewords:
        print v
    print '\n\n\n\n\n\n'

with open('top5wordsfile', 'w+') as fw:
    fw.write(kv_string)
