# coding: utf-8

# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys, traceback
import time

def get_links(browser, link):
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # browser = webdriver.PhantomJS('/usr/local/nvm/versions/node/v9.2.0/lib/node_modules/phantomjs-prebuilt/bin/phantomjs', desired_capabilities=dcap)

    browser.get(link)

    # load more
    # TODO: error if cannot load more
    load_more = browser.execute_script("return document.getElementsByClassName('_1cr2e _epyes')")

    if len(load_more) > 0:
        load_more[0].click()

    for i in range(0, 10):
        try:
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            break

    data = browser.execute_script("return document.getElementsByClassName('_mck9w _gvoze _f2mse')")

    links = []
    for d in data:
        try:
            links.append(d.find_elements_by_xpath(".//a")[0].get_attribute("href"))
        except Exception as e:
            traceback.print_exc(file=sys.stderr)

    return links
