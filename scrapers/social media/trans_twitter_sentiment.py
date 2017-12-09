#usr/bin/python3

import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
"""
def getSentiment(txt):
	o = nlp.annotate(txt, properties={"annotators":"sentiment", "outputFormat":"json"})
	sval = 0.0
	norm = 2
	if(len(o['sentences']) == 0):
		return 0
	for sentence in o['sentences']:
		st = int(sentence['sentimentValue'])
		sval += float(st - norm)
	return float(sval)/len(o['sentences'])

nlp = StanfordCoreNLP('http://localhost:9000')
"""
with open("trans_pipe/translated_tweets", "r") as fl:
	tweets = fl.read().split("\n")

"""
tweets = [list(filter(lambda x: x!=',', re.split(r"(,(?=\S))", s))) for s in tweets]

tweets_sentiment = []

for i, t in enumerate(tweets):
	if(len(t) < 3):
		continue
	tweets_sentiment.append(t + [str(getSentiment(t[2][1:-1]))])

with open("translated_tweets_sentiment", "w+") as fw:
	fw.write("\n".join([",".join(t) for t in tweets_sentiment]))
"""


