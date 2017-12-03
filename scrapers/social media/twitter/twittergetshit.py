from sklearn.feature_extraction.text import TfidfVectorizer
import hashlib
from sklearn.externals import joblib
import numpy
from operator import itemgetter
from itertools import groupby
with open("processed_tweets.csv", "r") as fl:
    all_content = fl.read().split("\n")

all_content = [[w.replace("\"", "") for w in t.split(",")] for t in all_content]

tweets = [(t[1], t[2]) for t in all_content if len(t) > 4 and t[3].lower() =="tweet"]
bios = [t[2] for t in all_content if len(t) > 4 and t[3].lower() == "bio"]

tweetsGrouped = [(k, len([x for x,y in g])) for k,g in groupby(tweets, key=itemgetter(0))]
tweetsGrouped.sort(key=itemgetter(1), reverse=True)
print(len(tweetsGrouped))
tweetvectorizer = TfidfVectorizer(stop_words="english")
tweetvectorizer.fit_transform(tweets)
#joblib.dump(tweetvectorizer, "tweetvector")

biovectorizer = TfidfVectorizer(stop_words="english")
biovectorizer.fit_transform(tweets)
#joblib.dump(biovectorizer, "biovector")

vecs = tweetvectorizer.transform(tweets)
#vecs = [numpy.asarray(v.T) for v in vecs]
# dup_tuples = []
# similarity_thresh = 0.95
#
# for i, v1 in enumerate(vecs):
#     for j, v2 in enumerate(vecs):
#         if i == j:
#             continue
#
#         dp = numpy.dot(v1, v2.T)
#         if dp > similarity_thresh:
#             print("Similar")
#             dup_tuples.append((i,j))
#         else:
#             print("Not similar")
#             print("Not similar")
# print(dup_tuples)


