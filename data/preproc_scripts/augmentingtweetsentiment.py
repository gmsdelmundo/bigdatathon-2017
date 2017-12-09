#usr/bin/python3
import numpy as np
import operator
import re

with open("product_cosine_similarity_scores.csv", "r") as fl:
	mat = fl.read().split("\n")

prod_ord = mat[0]
mat = mat[1:]
similarity_dict = {}
for rt in mat:
	r = rt.split(",")
	prodid = r[-1]
	similarity_dict[prodid] = np.array([float(i) for i in r[:-1]])

def getNSimilar(prodid, n):
	if prodid not in similarity_dict:
		return None
	vec = similarity_dict[prodid]
	dtmp = []
	mag = np.linalg.norm(vec)
	for k, v in similarity_dict.items():
		if k == prodid:
			continue
		dp = np.dot(vec, v) / (mag * np.linalg.norm(v))
		print(dp)
		dtmp.append([k, dp])
	dtmp_sorted = sorted(dtmp, key=operator.itemgetter(1), reverse=True)
	items = [t[0] for t in dtmp_sorted[:n]]
	return items

with open("translatedtweetssentiment.txt", "r") as fl:
	tweets = fl.read().split("\n")

tweets = [list(filter(lambda x: x!=',', re.split(r"(,(?=\S))", s))) for s in tweets]

tweets_new = []
N = 5
for i, t in enumerate(tweets):
	tweets_new.append(t)
	similar_items = getNSimilar(t[1], N)
	if similar_items is None:
		continue
	for s in similar_items:
		tweets_new.append([t[0], s, "", t[3], t[4]])

with open("sentiment_augmented", "w+") as fw:
	fw.write("\n".join([",".join(t) for t in tweets_new]))

	
		
		

	

