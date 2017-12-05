import torch
import torch.nn as nn
from torchvision import models
import numpy as np

number_of_images = 5
matrix_of_similarities = np.zeros(shape=(number_of_images, number_of_images))

test_vector = [1,2,3,4,5]
feature_vector = []

for i in range(number_of_images):
	for j in range (number_of_images):

	#input image into model here

	#get last layer of model here
		
	matrix_of_similarities[i][j] = #calculate similarity score here
	



#TODO:
#Lucas - Feed images from file into Inception model
#Hilda - Set up model and get last layer of it (called feature vector)
#Tushar - Take feature vectors and 
