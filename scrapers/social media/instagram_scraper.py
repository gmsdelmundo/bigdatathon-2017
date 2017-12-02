
# coding: utf-8

# In[4]:



from pyspark import SparkContext
sc = SparkContext()


# In[1]:


import pandas as pd
from urllib import request
import re
import json
from pprint import pprint as pp


# In[2]:


from selenium import webdriver
browser = webdriver.Firefox()
type(browser)


# In[7]:


import platform
from bs4 import BeautifulSoup
from selenium import webdriver

# PhantomJS files have different extensions
# under different operating systems
if platform.system() == 'Windows':
    PHANTOMJS_PATH = './phantomjs.exe'
else:
    PHANTOMJS_PATH = './phantomjs'


# here we'll use pseudo browser PhantomJS,
# but browser can be replaced with browser = webdriver.FireFox(),
# which is good for debugging.
browser = webdriver.PhantomJS('/usr/local/bin/phantomjs')
browser.get('https://www.instagram.com/gucci/')

# let's parse our html
soup = BeautifulSoup(browser.page_source, "html.parser")
# get all the games
print(soup)
games = soup.find_all('tr', {'class': 'stage-finished'})

# and print out the html for first game


# In[10]:


##r = requests.get("https://www.instagram.com/yungchiwing/?hl=en")
##soup = BeautifulSoup(r.content)
js = soup.find("script",text=re.compile("window._sharedData")).text
_json = json.loads((js[js.find("{"):js.rfind("}")+1]))
_json


# In[16]:



_json['country_code']

