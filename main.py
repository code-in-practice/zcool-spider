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



renqidom = bodysoup.find(attrs={'class': 'f20 cf90'}).string
print('-----------------------------------------------------------')
print(renqidom)
