# coding: utf-8

# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys, traceback
import time

def scrape(browser, link, LINK):
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # browser = webdriver.PhantomJS('/usr/local/nvm/versions/node/v9.2.0/lib/node_modules/phantomjs-prebuilt/bin/phantomjs', desired_capabilities=dcap)

    browser.get(link)

    # load more comments
    data = browser.execute_script("return document.getElementsByClassName('_m3m1c _1s3cd')")
    while len(data) > 0:
        try:
            # TODO: error if cannot load more
            data[0].click()
            data = browser.execute_script("return document.getElementsByClassName('_m3m1c _1s3cd')")
            time.sleep(1)
        except Exception as e:
            traceback.print_exc(file=sys.stderr)

    # comments
    comments = browser.execute_script("return document.getElementsByClassName('_ezgzd')")
    results = []
    for comment in comments:
        texts = comment.find_elements_by_xpath(".//span/span")
        result = ''
        for text in texts:
            result = result + text.get_attribute("innerHTML")
        results.append(result)

    image_div = browser.execute_script("return document.getElementsByClassName('_4rbun')")
    image = image_div[0].find_elements_by_xpath(".//img")[0]
    image_src = image.get_attribute("src")

    likes = "0"
    likes_div = browser.execute_script("return document.getElementsByClassName('_nzn1h')")
    if likes_div and len(likes_div) > 0:
       likes_span = likes_div[0].find_elements_by_xpath(".//span")
       if likes_span and len(likes_span) > 0:
          likes = likes_span[0].get_attribute("innerHTML")

    final = {
        "comments": results,
        "image_src": image_src,
        "likes": likes,
        "link": link,
        "hashtag": LINK
    }

    return final
