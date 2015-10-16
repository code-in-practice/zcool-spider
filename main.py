import requests
from bs4 import BeautifulSoup

url = 'http://www.zcool.com.cn/u/1'
r = requests.get(url)
bodydom = r.content
# print(bodydom)
bodysoup = BeautifulSoup(bodydom)
namedom = bodysoup.find('div', class_='vm ubcTitle').text.strip()
print(namedom)
renqidom = bodysoup.find(attrs={'class': 'f20 cf90'}).text.strip()
print(renqidom)
