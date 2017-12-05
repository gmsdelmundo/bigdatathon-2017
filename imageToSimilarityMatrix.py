import torch
from torch.autograd import Variable
import torch.nn as nn
from torchvision import models
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import csv
from torchvision.transforms import ToTensor


number_of_images = 5
matrix_of_similarities = np.zeros(shape=(number_of_images, number_of_images))

test_vector = [1,2,3,4,5]


v3 = models.inception_v3(pretrained=True)
without_final_layer = nn.Sequential(*list(v3.children())[:-1])
v3.classifier = without_final_layer

file_with_image_urls = "http:///Users/BlackHawk/Desktop/Fashion_BigDatathon/scrapers/social media/twitter/kv-data"
with open('/Users/BlackHawk/Desktop/Fashion_BigDatathon/scrapers/social media/twitter/kv-data.csv', 'r') as file_with_image_urls: 
	_file = csv.reader(file_with_image_urls)
# Go through the links in the file and put them through the model to get features
	for row in _file:
		link_row = row[8]
		link = link_row[8:]
		print(link)

		response = requests.get(link)
		img = Image.open(BytesIO(response.content))

		print("testing model...")
		img = ToTensor()(img).unsqueeze(0) # unsqueeze to add artificial first dimension
		output = v3(Variable(img))

		
#get_feature_vector 

for i in range(number_of_images):
	for j in range (number_of_images):
		

	#get last layer of model here
	
		
		matrix_of_similarities[i][j] = 0#calculate similarity score here




