import requests
from bs4 import BeautifulSoup

url = 'http://www.zcool.com.cn/u/1'
r = requests.get(url)
bodydom = r.content
# print(bodydom)
bodysoup = BeautifulSoup(bodydom, 'html.parser')
username = bodysoup.find(attrs= {'class': 'ubcTitle'}).span.text.strip()
print('username: ' + username)

city = bodysoup.find(attrs= {'class': 'ubcTitle'}).next_sibling.next_sibling.text.strip().split('/')[0].strip()
print('city: ' + city)

profession = bodysoup.find(attrs= {'class': 'ubcTitle'}).next_sibling.next_sibling.text.strip().split('/')[1].strip()
print('profession: ' + profession)

signature = bodysoup.find(attrs= {'class': 'nanBox'}).p.text.strip()
print('signature: ' + signature)

popularity = bodysoup.findAll(attrs={'class': 'f20 cf90'})[0].text.strip()
print('popularity: ' + popularity)

score = bodysoup.findAll(attrs={'class': 'f20 cf90'})[1].text.strip()
print('score: ' + score)

follower_number = bodysoup.findAll(attrs={'class': 'f20 cf90'})[2].text.strip()
print('follower_number: ' + follower_number)

follow_number = bodysoup.findAll(attrs={'class': 'f20 cf90'})[3].text.strip()
print('follow_number: ' + follow_number)
