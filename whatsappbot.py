from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import time
contact = "Int()"
text = "Hello, niggers! "
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
print("Scan QR Code, And then Enter")
input()
print("Logged In")
xpath='//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]'
input_box_search = WebDriverWait(driver,50).until(lambda driver: driver.find_element('xpath',xpath))
input_box_search.click()
time.sleep(2)
input_box_search.send_keys(contact)
time.sleep(2)
chat_xpath='//span[@title="Int()"]'
contact=driver.find_element('xpath',chat_xpath)
contact.click()
for i in range(500):
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
    input_box = driver.find_element('xpath',inp_xpath)
    input_box.send_keys(text + Keys.ENTER)
driver.quit()