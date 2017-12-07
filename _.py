from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
import csv

data_dir = '/Users/tusharjain/code/bigdatathon-2017/data/kv-data-hashed-forvictor'
file_dir = '/Users/tusharjain/code/bigdatathon-2017/models/research/slim/'
output_file = 'pre_dot.csv'
input_file = '/Users/tusharjain/code/bigdatathon-2017/pre_dot.csv'
output_file_result = 'fml2.csv'

def make_brand_dict():
	with open(data_dir, 'r') as file_with_image_urls:
		rows = csv.reader(file_with_image_urls)
		next(rows, None)
		brands_dictionary = {}
		for row in rows:
			brand = row[3]
			if brand not in brands_dictionary:
				brands_dictionary[brand] = True
		return brands_dictionary

def get_feature_vector_ends():
	append_me = {}
	with open(data_dir, 'r') as file_with_image_urls:
		rows = csv.reader(file_with_image_urls)
		next(rows, None)
		for row in rows:
			price = row[4][3:]
			content_hash = row[9]
			brand = row[3]

			append_me[content_hash] = {
				"price": float(price)/57000,
				"brand": brand
			}

	return append_me

def pre_dot():
	dfs = []
	for i in range(12):
		df = pd.read_csv(file_dir + 'all_' + str(i) + '.csv')
		dfs.append(df)
	df = pd.concat(dfs)
	df = df.set_index("hash")

	brands_dictionary = make_brand_dict()
	for key in brands_dictionary.keys():
		df[key] = 0

	feature_vector_ends = get_feature_vector_ends()
	for i, row in df.iterrows():
		end = feature_vector_ends[i]
		price = end["price"]
		brand = end["brand"]
		df.loc[i, "price"] = price
		df.loc[i, brand] = 1
	return df

def get_similarity_scores(df):
	columns = df.shape[1]
	rows = df.shape[0]
	print("number of features", columns)
	print("number of rows", rows)
	similarity_matrix = np.zeros(shape=(rows, rows))
	for i, vec1 in df.iterrows():
		for j, vec2 in df.iterrows():
			dot = np.dot(vec1, vec2)
			score = dot/((np.linalg.norm(vec1)*np.linalg.norm(vec2)))
			print(i, j, "similarity score", score)
			similarity_matrix[i][j] = score	
	return similarity_matrix	

# df = pre_dot()
# df.to_csv(output_file)

df = pd.read_csv(input_file)
df_drop = df.drop(['product_id', 'hash'], axis=1)
result = get_similarity_scores(df_drop)

df_result = pd.DataFrame(result)
df_result.to_csv(output_file_result)
