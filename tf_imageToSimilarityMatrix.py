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

urls = get_urls()
result_logits = get_features_vectors(urls)
write_feature_vectors(result_logits)

# TODO: add feature basis
# TODO: calculate similarity matrix
