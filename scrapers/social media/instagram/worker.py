import sys, traceback, time

import json

from get_links import get_links
from scrape import scrape

def worker(browser, LINK):
  links = []
  try:
    links = get_links(browser, LINK)
  except Exception as e:
    traceback.print_exc(file=sys.stderr)

  for link in links:
    try:
      value = scrape(browser, link, LINK)
      print(json.dumps(value, indent=2) + ',')
      time.sleep(1)
    except Exception as e:
      traceback.print_exc(file=sys.stderr)
