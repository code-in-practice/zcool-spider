import requests
from bs4 import BeautifulSoup

user_id = 1
ajax_param = {'id': user_id}
ajax_url = 'http://www.zcool.com.cn/getPersonDetailInfo.do?jsonpCallback=?'
r = requests.post(ajax_url, data=ajax_param)
#print(r.content)
bodydom = r.content
bodysoup = BeautifulSoup(bodydom, 'html.parser')

username = bodysoup.find_all('td')[0].text.strip().split('\n')[0].strip()
print('username: ' + username)

gender = bodysoup.find_all('td')[0].text.strip().split('\n')[1].strip()
print('gender: ' + gender)

hometown = bodysoup.find_all('td')[1].text.strip()
print('hometown: ' + hometown)
