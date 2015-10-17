#coding=utf-8
import requests
from bs4 import BeautifulSoup
import json


def main_user(user_id):
    url = 'http://www.zcool.com.cn/u/1'
    r = requests.get(url)
    bodydom = r.content

    bodysoup = BeautifulSoup(bodydom, 'html.parser')

    i=0
    keys = ['popularity', 'score', 'follower_number', 'follow_number']
    user_detail_dict = {}

    username = bodysoup.find(attrs= {'class': 'ubcTitle'}).span.text.strip()
    city = bodysoup.find(attrs= {'class': 'ubcTitle'}).next_sibling.next_sibling.text.strip().split('/')[0].strip()
    profession = bodysoup.find(attrs= {'class': 'ubcTitle'}).next_sibling.next_sibling.text.strip().split('/')[1].strip()
    signature = bodysoup.find(attrs= {'class': 'nanBox'}).p.text.strip()

    user_detail_dict.update({'username': username})
    user_detail_dict.update({'city': city})
    user_detail_dict.update({'profession': profession})
    user_detail_dict.update({'signature': signature})

    for w in bodysoup.find_all(attrs={'class': 'f20 cf90'}):
        user_detail_dict.update({keys[i]: w.text.strip()})
        i = i+1

    return user_detail_dict

def ajax_user(user_id):
    ajax_param = {'id': user_id}
    ajax_url = 'http://www.zcool.com.cn/getPersonDetailInfo.do?jsonpCallback=?'
    r = requests.post(ajax_url, data=ajax_param)
    bodydom = r.content
    bodysoup = BeautifulSoup(bodydom, 'html.parser')

    i=0
    keys = ['realname', 'hometown', 'mobile', 'last_login', 'birthday', 'address_city', 'qq', 'zcool_age', 'college', 'email', 'wechat', 'equipments', 'tags', 'description', 'links']
    user_detail_dict = {}
    user_detail_dict.update({'id': user_id})

    # check if the user is available
    status = r.status_code == 200
    print(status)

    if status:
        for w in bodysoup.find_all('td'):
            user_detail_dict.update({keys[i]: w.text.strip().split(u'：')[1].replace('\t', '')})
            i = i+1
        return user_detail_dict
    else:
        return False

def zcool_user_info(user_id):

    user_detail_ajax_dict = ajax_user(user_id)

    if user_detail_ajax_dict:
        user_detail_ajax_json = json.dumps(user_detail_ajax_dict, indent=4,ensure_ascii=False).encode('utf8')
        user_detail_main_dict = main_user(user_id)
        user_detail_mail_json = json.dumps(user_detail_main_dict, indent=4,ensure_ascii=False).encode('utf8')
        user_detail_dict = user_detail_main_dict.copy()
        user_detail_dict.update(user_detail_ajax_dict)
        return user_detail_dict
    else:
        return False



for i in xrange(1, 10000):
    user_id = i
    user_detail_dict = zcool_user_info(user_id)
    if user_detail_dict:
        user_detail_json = json.dumps(user_detail_dict, indent=4,ensure_ascii=False).encode('utf8')
        print(user_detail_json)
    else:
        print('user: ' + str(user_id) + ' does not exist ------------------------------------')



