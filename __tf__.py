# clone this and run inside this folder
# https://github.com/tensorflow/models/tree/master/research/slim
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import multiprocessing
import time

import csv

try:
	import urllib2 as urllib
except ImportError:
	import urllib.request as urllib

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib import slim

from nets import inception_v3
from preprocessing import inception_preprocessing

args = sys.argv[1:]
number_chunk = args[0]
output_file = 'all_' + number_chunk + '.csv'

image_size = inception_v3.inception_v3.default_image_size
checkpoints_dir = '/Users/tusharjain/code/bigdatathon-2017'
data_dir = '/Users/tusharjain/code/bigdatathon-2017/data/kv-data-hashed-forvictor'
old_data_dir = '/Users/tusharjain/code/bigdatathon-2017/models/research/slim/matrix.csv'
# old_data_dir = '/code/models/research/slim/matrix.csv'
# checkpoints_dir = '/tmp/checkpoints'
# data_dir = '/code/data/kv-data-hashed-forvictor'

def get_features_vector(url):
	try:
		with tf.Graph().as_default():
			image_string = urllib.urlopen(url).read()
			image = tf.image.decode_jpeg(image_string, channels=3)
			processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
			processed_images = tf.expand_dims(processed_image, 0)

			with slim.arg_scope(inception_v3.inception_v3_arg_scope()):
				logits, _ = inception_v3.inception_v3(processed_images, num_classes=1001, is_training=False)

			init_fn = slim.assign_from_checkpoint_fn(
				os.path.join(checkpoints_dir, 'inception_v3.ckpt'),
				slim.get_model_variables('InceptionV3')
			)

			with tf.Session() as sess:
				init_fn(sess)
				np_logits = sess.run([logits])
				return np_logits
	except Exception as e:
		print(e)

def write_feature_vectors(result_logits):
	product_ids = [d["product_id"] for d in result_logits]
	hashes = [d["hash"] for d in result_logits]
	np_logits = np.array([d["np_logits"][0].squeeze() for d in result_logits])
	df = pd.DataFrame(np_logits)
	df["product_id"] = product_ids
	df["hash"] = hashes 
	df = df.set_index("hash")
	df.to_csv(output_file)

def get_urls():
	urls = []
	with open(data_dir, 'r') as file_with_image_urls:
		rows = csv.reader(file_with_image_urls)
		for row in rows:
			url = row[8]
			product_id = row[0]
			content_hash = row[9]
			urls.append({
				"url": url,
				"product_id": product_id,
				"hash": content_hash
			})
	return urls

def worker_main(work_queue, result_queue):
	i = 0
	pid = os.getpid()
	while True:
		print("loop", i, "pid", pid)
		try:
			if work_queue.empty():
				break
			url_dict = work_queue.get()
			np_logits = get_features_vector(url_dict["url"])
			if np_logits:
				d = {
					"url": url_dict["url"],
					"product_id": url_dict["product_id"],
					"hash": url_dict["hash"],
					"np_logits": np_logits
				}

				result_queue.put(d)
				print("number", i, "pid", pid, "hash", d["hash"], np_logits)
			else:
				print("no np_logits")
		except Exception as e:
			print(e)
		i += 1

def do_it(urls):
	i = 0
	result_logits = []
	for url_dict in urls:
		try:
			np_logits = get_features_vector(url_dict["url"])
			if np_logits:
				d = {
					"url": url_dict["url"],
					"product_id": url_dict["product_id"],
					"hash": url_dict["hash"],
					"np_logits": np_logits
				}

				result_logits.append(d)
				print("number", i, "hash", d["hash"], np_logits)
			else:
				print("no np_logits")
		except Exception as e:
			print(e)
		i += 1

	return result_logits

# product_ids = {}
# with open(old_data_dir, 'r') as f:
# 	rows = csv.reader(f)
# 	for row in rows:
# 		product_id = row[9]
# 		product_ids[product_id] = True
# urls = list(filter(lambda d: d["hash"] not in product_ids, get_urls()))
urls = get_urls()

print("pid", os.getpid())
print("number of urls", len(urls), "chunk number", number_chunk, "output file", output_file)
chunks = [urls[i:i + 50] for i in range(0, len(urls), 50)]
result_logits = do_it(chunks[int(number_chunk)])

# print("master pid", os.getpid())

# number_cpu = range(multiprocessing.cpu_count())
# print("number of cpu", number_cpu)

# result_queue = multiprocessing.Queue()
# work_queue = multiprocessing.Queue()

# for url in urls[1:35]:
# 	work_queue.put(url)

# processes = [multiprocessing.Process(target=worker_main, args=(work_queue, result_queue,)) for i in number_cpu]

# for process in processes:
# 		process.start()
# for process in processes:
# 		process.join()

# result_logits = []
# i = 0
# while True:
# 	print("item number got from queue", i)
# 	if result_queue.empty():
# 		break
# 	result_logits.append(result_queue.get())
# 	i += 1

write_feature_vectors(result_logits)
