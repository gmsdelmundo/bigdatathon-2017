from bs4 import BeautifulSoup
from selenium import webdriver

browser = webdriver.PhantomJS('/usr/local/nvm/versions/node/v9.2.0/lib/node_modules/phantomjs-prebuilt/bin/phantomjs')
browser.get('https://instagram.com')

soup = BeautifulSoup(browser.page_source, "html.parser")
print(soup)

