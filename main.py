import requests
from bs4 import BeautifulSoup

url = 'http://www.zcool.com.cn/u/1'
r = requests.get(url)
bodydom = r.content
# print(bodydom)
bodysoup = BeautifulSoup(bodydom, 'lxml')
namedom = bodysoup.find('div', class_='vm ubcTitle')
print(namedom)
# namesoup = BeautifulSoup(namedom)
# name = namesoup.get_text()
# print(name)



renqidom = bodysoup.find('span', class_='f20 cf90')
print('-----------------------------------------------------------')
print(renqidom)
