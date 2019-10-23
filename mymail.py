from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client['mymail']
collection = db['mails']

driver = webdriver.Chrome()

driver.get('https://mail.yandex.ru/')
mail_enter = driver.find_element_by_class_name('HeadBanner-Button-Enter')
mail_enter.send_keys(Keys.RETURN)

assert "Авторизация" in driver.title

login = driver.find_element_by_id('passp-field-login')
login.send_keys('thedark-ride')
login.send_keys(Keys.RETURN)
pwd = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.ID, 'passp-field-passwd'))
        )
pwd.send_keys('Nothingbutwind!')
pwd.send_keys(Keys.RETURN)

mails = WebDriverWait(driver,5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'mail-MessageSnippet-Wrapper'))
        )
for mail in mails:
    item = {}
    item['link'] = mail.find_element_by_css_selector('a.mail-MessageSnippet').get_attribute('href')
    item['sender'] = mail.find_element_by_css_selector('span.mail-MessageSnippet-FromText').get_attribute('innerText')
    item['theme'] = mail.find_element_by_css_selector('span.mail-MessageSnippet-Item_subject span').get_attribute('innerText')
    item['date'] = mail.find_element_by_css_selector('span.mail-MessageSnippet-Item_dateText').get_attribute('title')
    driver.get(item['link'])

    print(item)
    collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)

driver.quit()
