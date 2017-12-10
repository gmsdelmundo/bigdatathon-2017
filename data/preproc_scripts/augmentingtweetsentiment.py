#usr/bin/python3
import numpy as np
import operator
import re

with open("product_cosine_similarity_scores.csv", "r") as fl:
	mat = fl.read().split("\n")

prod_ord = mat[0].split(",")
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
	for i in range(len(vec)):
		if prodid == prod_ord[i]:
			continue
		dtmp.append((prod_ord[i], vec[i]))
	dtmp_sorted = sorted(dtmp, key=operator.itemgetter(1), reverse=True) 
	return dtmp_sorted[:n]

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
		print(s[1])
		tweets_new.append([t[0], s[0], "", str(float(t[3]) * s[1]), t[4]])

with open("sentiment_augmented", "w+") as fw:
	fw.write("\n".join([",".join(t) for t in tweets_new]))

	
		
		

	

