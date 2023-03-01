import requests
from bs4 import BeautifulSoup
import re
import json
from fake_useragent import UserAgent

ua = UserAgent()
my_json = []
url = 'https://spb.hh.ru/search/vacancy'

for i in range(0, 101):
    headers = {
        'User-Agent': ua.random
        }
    params = {
        'text': 'python',
        'area': [1, 2],
        'page': i,
        'hhtmFrom': 'vacancy_search_list',
        'items_on_page':'20'
    }
    req = requests.get(url=url, headers=headers, params=params)
    soup = BeautifulSoup(req.text, 'lxml')
    serp_items = soup.find_all(class_="serp-item")
    for item in serp_items:
        my_dict = {}
        link = item.find('a').get('href')
        req2 = requests.get(url=link, headers=headers)
        soup2 = BeautifulSoup(req2.text, 'lxml')
        try:
            description = soup2.find(attrs={"class": [
                                                "vacancy-branded-user-content", 
                                                "vacancy-description"
                                                ]}).text
            key1 = re.search(r'[Dd]jango', description)
            key2 = re.search(r'[Ff]lask', description)
            if key1 and key2:
                my_dict['company'] = soup2.find('a', attrs={"data-qa": "vacancy-company-name"}).text
                my_dict['city'] = soup2.find(attrs={"data-qa": ["vacancy-view-location", "vacancy-view-link-location"]}).text
                my_dict['salary'] = soup2.find(attrs={"data-qa": "vacancy-salary"}).text
                my_dict['link'] = link
                my_json.append(my_dict)
        except Exception as ex:
            # print(link)
            # print(ex)
            pass
        
with open('data.json', 'w') as file:
    json.dump(my_json, file, indent=4, ensure_ascii=False)
