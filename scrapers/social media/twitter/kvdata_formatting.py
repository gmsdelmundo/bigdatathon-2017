import csv
import re

regex = r'(.+):(.+)'

columns = []
data = []
with open("kv-data-hashed2", "r") as fl:
	data = fl.read().split("\n")
data = [r.split(",") for r in data]
print(data[0])
for i in data[0]:
	cname = re.match(regex, i)[1]
	while ":" in cname:
		cname = re.match(regex, cname)[1]
	columns.append(cname)

print(columns)
newdata = []
newdata.append(columns)
for row in data:
	print(len(columns))
	print(len(row))
	print(row)
	print(len(row) == len(columns))
	for i, r in enumerate(row):
		row[i] = row[i].replace(columns[i]+":", "", 1)
	newdata.append(["\""+r+"\"" for r in row])

with open("kv-data-hashed-forvictor", "w+") as fw:
	fw.write("\n".join(
		[",".join(d) for d in newdata]
	))

	

