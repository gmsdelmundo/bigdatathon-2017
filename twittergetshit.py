from sklearn.feature_extraction.text import TfidfVectorizer
import hashlib
from sklearn.externals import joblib
import numpy
from operator import itemgetter
from itertools import groupby
import json

print("Testing... 1")
with open("/Users/BlackHawk/Desktop/Fashion BigDatathon/bigdatathon-2017/scrapers/social media/twitter/processed_tweets.csv", "r") as fl:
    all_content = fl.read().split("\n")

google_file = open("/Users/BlackHawk/Desktop/Fashion BigDatathon/bigdatathon-2017/googledata.json")
google_data = json.loads(google_file)

print("Testing... A")

all_content = [[w.replace("\"", "") for w in t.split(",")] for t in all_content]

tweets = [(t[1], t[2]) for t in all_content if len(t) > 4 and t[3].lower() =="tweet"]
bios = [t[2] for t in all_content if len(t) > 4 and t[3].lower() == "bio"]

print("Testing... B")

tweetsGrouped = [(k, len([x for x,y in g])) for k,g in groupby(tweets, key=itemgetter(0))]
tweetsGrouped.sort(key=itemgetter(1), reverse=True)
print(len(tweetsGrouped))
tweetvectorizer = TfidfVectorizer(stop_words="english")
tweetvectorizer.fit_transform(tweets)
#joblib.dump(tweetvectorizer, "tweetvector")

print("Testing... C")

biovectorizer = TfidfVectorizer(stop_words="english")
biovectorizer.fit_transform(tweets)
#joblib.dump(biovectorizer, "biovector")

vecs = tweetvectorizer.transform(tweets)

#all_content.count()
