# clone this and run inside this folder
# https://github.com/tensorflow/models/tree/master/research/slim
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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

image_size = inception_v3.inception_v3.default_image_size
checkpoints_dir = '/tmp/checkpoints'

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

# def get_features_vectors(urls):
# 	result_logits = {}
# 	for i in range(len(urls)):
# 		url = urls[i]
# 		np_logits = get_features_vector(url)
# 		result_logits[url] = np_logits
# 		print(i, url)
# 		print(np_logits)
# 	return result_logits

def write_feature_vectors(result_logits):
	product_ids = [d["product_id"] for d in result_logits]
	np_logits = np.array([d["np_logits"][0].squeeze() for d in result_logits])
	df = pd.DataFrame(np_logits)
	df["product_id"] = product_ids
	df = df.set_index("product_id")
	df.to_csv('matrix.csv')

def get_urls():
	urls = []
	with open('/code/data/kv-data-hashed-forvictor', 'r') as file_with_image_urls:
		rows = csv.reader(file_with_image_urls)
		for row in rows:
			url = row[8]
			product_id = row[0]
			urls.append({
				"url": url,
				"product_id": product_id
			})
	return urls

def worker_main(work_queue, result_queue):
	while True:
		if work_queue.empty():
			break
		url_dict = work_queue.get()
		np_logits = get_features_vector(url_dict["url"])

		d = {
			"url": url_dict["url"],
			"product_id": url_dict["product_id"],
			"np_logits": np_logits
		}

		result_queue.put(d)
		print(d)
		work_queue.task_done()

result_queue = multiprocessing.Queue()
work_queue = multiprocessing.JoinableQueue()

urls = get_urls()
for url in urls[1:]:
	work_queue.put(url)

work_pool = multiprocessing.Pool(4, worker_main, (work_queue, result_queue,))
work_queue.join()

result_logits = []
while True:
	if result_queue.empty():
		break
	result_logits.append(result_queue.get())

write_feature_vectors(result_logits)

# TODO: add feature basis
# TODO: calculate similarity matrix
