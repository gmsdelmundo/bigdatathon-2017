import multiprocessing
import os
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from worker import worker

the_queue = multiprocessing.JoinableQueue()

def worker_main(queue):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    browser = webdriver.PhantomJS('/usr/local/nvm/versions/node/v9.2.0/lib/node_modules/phantomjs-prebuilt/bin/phantomjs', desired_capabilities=dcap)
    while True:
        LINK = queue.get(True)
        worker(browser, LINK)
        queue.task_done()

the_pool = multiprocessing.Pool(10, worker_main, (the_queue,))

LINKS = [
  "https://www.instagram.com/explore/tags/leopardprintcoat",
  "https://www.instagram.com/explore/tags/reversiblepufferjacket",
  "https://www.instagram.com/explore/tags/sneakermules",
  "https://www.instagram.com/explore/tags/weaveknitscarf",
  "https://www.instagram.com/explore/tags/coldshouldercrepemididress",
  "https://www.instagram.com/explore/tags/crepeminidress",
  "https://www.instagram.com/explore/tags/cliponaviatorsunglasses",
  "https://www.instagram.com/explore/tags/tripletotebag",
  "https://www.instagram.com/explore/tags/autumnprinthoodie",
  "https://www.instagram.com/explore/tags/classicdenimjacket"
]

for L in LINKS:
    the_queue.put(L)

the_queue.join()