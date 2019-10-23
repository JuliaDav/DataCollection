from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client['mvideo']
collection = db['bestsellers']

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru')

bestsellers = driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]')
while True:
    try:
        button = WebDriverWait(bestsellers,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')
                                           ))

        driver.execute_script("$(arguments[0]).click();", button)
    except:
        print('Сбор закончен')
        break

goods = bestsellers.find_elements_by_css_selector('li.gallery-list-item')

for good in goods:
    item = {}
    item['name'] = good.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('innerHTML')
    item['link'] = good.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('href')
    item['price'] = good.find_element_by_css_selector('div.c-pdp-price__current').get_attribute('innerText').replace('\xa0','').replace('¤','')
    print(item)

    collection.update_one({'link': item['link']}, {'$set':item}, upsert=True)

driver.quit()
