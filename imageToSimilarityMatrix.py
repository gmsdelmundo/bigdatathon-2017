import torch
import torch.nn as nn
from torchvision import models
import numpy as np

number_of_images = 5
matrix_of_similarities = np.zeros(shape=(500,500))

test_vector = [1,2,3,4,5]
feature_vector = []

for i in range(number_of_images):
	for j in range (number_of_images):
		j += i


	#input image into model here

	#get last layer of model here
		
		print("i is: " + i + " and j is: " + j)
		#matrix_of_similarities[i][j] = 10



#TODO:
#Lucas - Feed images from file into Inception model
#Hilda - Set up model and get last layer of it (called feature vector)
#Tushar - Take feature vectors and 
