import json
import pandas as pd
import numpy as np

with open('gg.json', 'r') as f:
	data = json.load(f)
	brands_location = data["brands"]["location"]
	brands_time = data["brands"]["location"]
	products_location = data["products"]["location"]
	products_time = data["products"]["location"]

	df_brands_location = pd.DataFrame(brands_location)
	df_products_location = pd.DataFrame(products_location)
	df_brands_time = pd.DataFrame(brands_time)
	df_products_time = pd.DataFrame(products_time)

	print(df_brands_location)
