import hashlib
import csv
kvdata = []
with open("kv-data", "r") as fl:
	kvdata = fl.read().split("\n")
kvdata = [[i for i in r.split(",")] for r in kvdata]

kvdata_hashed = []
for row in kvdata:
	if(len(row) <2):
		continue
	h = hashlib.md5(row[2][len("name:"):].encode()).hexdigest()
	kvdata_hashed.append(row+["hash:"+h])

with open("kv-data-hashed2", "w+") as fw:
	fw.write("\n".join([",".join(r) for r in kvdata_hashed]))

