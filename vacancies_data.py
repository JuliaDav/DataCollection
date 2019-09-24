from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import time
import pandas as pd

main_link_sj = 'https://www.superjob.ru'
main_link_hh = 'https://hh.ru/'
header = {'User-agent': 'Chrome/76.0.3809.132'}

# вводим нужную должность
name = input('Введите название вакансии:')
name_sj = name.replace(' ','%20')
name_hh = name.replace(' ', '+')
# формируем первые ссылки
html_sj = requests.get(f'{main_link_sj}/vacancy/search/?keywords={name_sj}', headers=header).text
parsed_html_sj = bs(html_sj,'html.parser')# для superjob
html_hh = requests.get(f'{main_link_hh}/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={name_hh}&page=0', headers=header).text
parsed_html_hh = bs(html_hh,'html.parser')# для headhunter

# дальше делим код на два блока:
# 1 блок для Superjob
# ищем количество страниц данных
pages_sj = parsed_html_sj.findAll('span',{'class':'qTHqo _2h9me DYJ1Y _2FQ5q _2GT-y'})
page_list_sj = []
for i in pages_sj:
    page_info = i.findChild().findChild().getText()
    page_list_sj.append(page_info)
# ищем максимальную страницу
try:
    max_page_sj = int(page_list_sj[-2])
except IndexError:
    max_page_sj = 1
# перебираем страницы с сайта superjob
vacancies_sj=[]
for page_n in range(max_page_sj):
    page = page_n + 1
    html = requests.get(f'{main_link_sj}/vacancy/search/?keywords={name_sj}&page={page}', headers=header).text
    parsed_html = bs(html, 'html.parser')
    vacancy_list = parsed_html.findAll('div',{'class':'_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
    for vac in vacancy_list:
        vac_data={}
        try:
            main_info = vac.find('div',{'class':'_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})
            vac_name = main_info.getText()
            vac_link = vac.find('div',{'class':'_3syPg _1_bQo _2FJA4'}).findChild().findChild()['href']
            compens_info = vac.find('span',{'class':'f-test-text-company-item-salary'}).getText()
            vac_data['name'] = vac_name
            vac_data['link'] = main_link_sj + vac_link
            vac_data['compensation'] = compens_info
            vac_data['from'] = 'superjob'
            vacancies_sj.append(vac_data)
        except AttributeError:
            pass
    time.sleep(2)


# 2 блок для HH
# ищем количество страниц данных
pages_hh = parsed_html_hh.findAll('a',{'class':'HH-Pager-Control'})
page_list_hh = []
for i in pages_hh:
    page_info = i.getText()
    page_list_hh.append(page_info)
# ищем максимальную страницу
try:
    max_page_hh = int(page_list_hh[-2])
except IndexError:
    max_page_hh = 1
# перебираем страницы
vacancies_hh=[]
for page_n in range(max_page_hh):
    page = page_n
    html = requests.get(f'{main_link_hh}/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={name_hh}&page={page}', headers=header).text
    parsed_html = bs(html,'html.parser')
    vacancy_block = parsed_html.find('div',{'class':'vacancy-serp'})
    vacancy_list = vacancy_block.findChildren(recursive=False)
    for vac in vacancy_list:
        vac_data={}
        try:
            main_info = vac.find('div',{'class':'resume-search-item__name'}).findChild().findChild()
            vac_name = main_info.getText()
            vac_link = main_info['href']
            compens_info = vac.find('div',{'class':'vacancy-serp-item__sidebar'}).getText().replace('\xa0', '')
            vac_data['name'] = vac_name
            vac_data['link'] = vac_link
            vac_data['compensation'] = compens_info
            vac_data['from'] = 'hh'
            vacancies_hh.append(vac_data)
        except AttributeError:
            pass
    time.sleep(2)

# два датафрейма для информации с каждого из сайтов, при необходимости можно их объединить, т.к. они полностью идентичны
df_hh = pd.DataFrame(vacancies_hh)
df_sj = pd.DataFrame(vacancies_sj)
print(df_hh)
print(df_sj)

