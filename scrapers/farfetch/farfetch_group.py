#usr/bin/python3

from itertools import groupby
import operator

with open("data/kv-data-hashed-forvictor.csv", "r") as fl:
	data = fl.read().split("\n")

data = [d.split(",") for d in data]
pdata = data[1:-1]
pdata = sorted(pdata, key=operator.itemgetter(9), reverse=True)
data_grouped = []
keys = []
for k, g in groupby(pdata, key=operator.itemgetter(9)):
	data_grouped.append(list(g)[0])

print(data_grouped[:20])

with open("data/kv-hashed-grouped.csv", "w+") as fl:
	fl.write(",".join(data[0]) + "\n")
	fl.write("\n".join([",".join(d) for d in data_grouped]))


