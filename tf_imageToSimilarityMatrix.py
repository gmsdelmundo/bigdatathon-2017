# clone this and run inside this folder
# https://github.com/tensorflow/models/tree/master/research/slim
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import csv

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib import slim

try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

from nets import inception_v3
from preprocessing import inception_preprocessing

image_size = inception_v3.inception_v3.default_image_size
checkpoints_dir = '/tmp/checkpoints'

def get_features_vectors(urls):
	result_logits = []
	for i in range(len(urls)):
			with tf.Graph().as_default():
					try:
							url = urls[i]
							image_string = urllib.urlopen(url).read()
							image = tf.image.decode_jpeg(image_string, channels=3)
							processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
							processed_images  = tf.expand_dims(processed_image, 0)

							with slim.arg_scope(inception_v3.inception_v3_arg_scope()):
											logits, _ = inception_v3.inception_v3(processed_images, num_classes=1001, is_training=False)

							probabilities = tf.nn.softmax(logits)

							init_fn = slim.assign_from_checkpoint_fn(
									os.path.join(checkpoints_dir, 'inception_v3.ckpt'),
									slim.get_model_variables('InceptionV3')
							)

							with tf.Session() as sess:
									init_fn(sess)
									np_image, np_logits, probabilities = sess.run([image, logits, probabilities])
									probabilities = probabilities[0, 0:]
									result_logits.append(np_logits)

							print(url)
							print(np_logits)

					except Exception as e:
							print(e)
							continue
	return result_logits

def write_feature_vectors(result_logits):
	result_logits_array = np.asarray(result_logits)
	shape = result_logits_array.shape
	df = pd.DataFrame(np.reshape(result_logits_array, (shape[0], shape[2])))
	df.to_csv('matrix.csv')

def get_urls():
	urls = []
	with open('/code/scrapers/social media/twitter/kv-data', 'r') as file_with_image_urls:
		rows = csv.reader(file_with_image_urls)
		for row in rows:
			url_row = row[8]
			url = url_row[8:]
			urls.append(url)
	return urls

def add_feature_vector_ends(feature_vectors):
	print("\n\nIn feature vector function.\n")
	append_me = []
	with open('/code/scrapers/social media/twitter/kv-data', 'r') as file_with_image_urls:
		rows = csv.reader(file_with_image_urls)
		for i, vector in enumerate(feature_vectors):
			print("Vector #: " + str(i) + " is: " + str(vector) + " and row is: " + str(rows[i]))
# want to append brand, price (normalized) 
			append_me.append(get_brand_dictionary(rows[i][3][7:]))
			append_me.append(double(rows[i][4][9:])/57000)	#divide by the max price to keep values between 1 and 0
			feature_vectors.append(append_me)
	return feature_vectors

def get_brand_dictionary(my_brand):
	print("\n\nIn get brand dictionary function\n")
	if not brands_dictionary:	#if brand vector has not yet been created, make it
		with open('/code/scrapers/social media/twitter/kv-data', 'r') as file_with_image_urls:
			rows = csv.reader(file_with_image_urls)
			i = 0
			for row in rows:
				brand_row = row[3]
				brand = brand_row[7:]
				if brand not in brands_dictionary:
					brands_dictionary[brand] = i
					i = i + 1
			if(len(brands_dictionary) != i):
				print("potential error in get_brand_dictionary")

	brand_vector = [0]*len(brands_dictionary)
	brand_vector[brands_dictionary[my_brand]] = 1
	return brand_vector


brands_dictionary = {}
urls = get_urls()
result_logits = get_features_vectors(urls)
write_feature_vectors(result_logits)
result_logits = add_feature_vector_ends(result_logits)




# TODO: add feature basis
# TODO: calculate similarity matrix
