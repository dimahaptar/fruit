import unittest
import selenium
import time
from selenium import webdriver

browser = webdriver.Chrome(
    executable_path='/usr/local/bin/chromedriver')
browser.get('https://www.google.com')
element = browser.find_element_by_id("lst-ib")
element.send_keys()
time.sleep(10)
browser.quit()
print("done")
