#coding=utf-8
import requests
from bs4 import BeautifulSoup

import json
from pymongo import MongoClient

from multiprocessing import Pool

from elasticsearch import Elasticsearch


def connect():
    db_url = '127.0.0.1'
    db_port = 27017
    client = MongoClient(db_url, db_port)

    db = client['zcool']
    collection = db['user']
    return collection

def main_user(user_id):
    url = 'http://www.zcool.com.cn/u/' + str(user_id)
    r = requests.get(url)
    bodydom = r.content

    bodysoup = BeautifulSoup(bodydom, 'html.parser')

    i=0
    keys = ['popularity', 'score', 'follower_number', 'follow_number']
    user_detail_dict = {}

    username_dom = bodysoup.find(attrs= {'class': 'ubcTitle'})
    if username_dom:
        username = bodysoup.find(attrs= {'class': 'ubcTitle'}).span.text.strip()
        city = bodysoup.find(attrs= {'class': 'ubcTitle'}).next_sibling.next_sibling.text.strip().split('/')[0].strip()
        profession = bodysoup.find(attrs= {'class': 'ubcTitle'}).next_sibling.next_sibling.text.strip().split('/')[1].strip()
        signature = bodysoup.find(attrs= {'class': 'nanBox'}).p.text.strip()

        user_detail_dict.update({'username': username.replace('\r\n', '')})
        user_detail_dict.update({'city': city.replace('\r\n', '')})
        user_detail_dict.update({'profession': profession.replace('\r\n', '')})
        user_detail_dict.update({'signature': signature.replace('\r\n', '')})

        for w in bodysoup.find_all(attrs={'class': 'f20 cf90'}):
            user_detail_dict.update({keys[i]: w.text.strip().replace('\r\n', '')})
            i = i+1

        return user_detail_dict
    else:
        return False


def ajax_user(user_id):
    ajax_param = {'id': user_id}
    ajax_url = 'http://www.zcool.com.cn/getPersonDetailInfo.do?jsonpCallback=?'
    r = requests.post(ajax_url, data=ajax_param)
    bodydom = r.content
    bodysoup = BeautifulSoup(bodydom, 'html.parser')

    i=0
    keys = ['realname', 'hometown', 'mobile', 'last_login', 'birthday', 'address_city', 'qq', 'zcool_age', 'college', 'email', 'wechat', 'equipments', 'tags', 'description', 'links']
    user_detail_dict = {}
    user_detail_dict.update({'_id': user_id})

    # check if the user is available
    status = r.status_code == 200

    if status:
        for w in bodysoup.find_all('td'):
            user_detail_dict.update({keys[i]: w.text.strip().split(u'：')[1].replace('\t', '').replace('\r\n', '')})
            i = i+1
        return user_detail_dict
    else:
        return False

def zcool_user_info(user_id):
    user_detail_ajax_dict = ajax_user(user_id)
    user_detail_main_dict = main_user(user_id)

    if user_detail_ajax_dict and user_detail_main_dict:

        user_detail_dict = user_detail_main_dict.copy()
        user_detail_dict.update(user_detail_ajax_dict)

        return user_detail_dict
    else:
        return False



collection = connect()
es = Elasticsearch()
def save_to_mongo(user_detail_dict):
    result = collection.find_one(user_detail_dict['_id'])
    if not result:
        object_id = collection.insert_one(user_detail_dict).inserted_id
        print(object_id)

    print(result)

def save_to_es(user_detail_dict):
    result = es.index(index="zcool", doc_type="user", id=user_detail_dict['_id'], body=user_detail_dict)
    print result

# results = collection.find()
# for result in results:
#     print(result)
#     del result['_id']
#     user_result_json = json.dumps(result, indent=4).encode('utf8')
#     print(user_result_json)

for user_id in xrange(1, 10000):
    user_detail_dict = zcool_user_info(user_id)
    if(user_detail_dict):
        print type(user_detail_dict)
        user_detail_json_str = json.dumps(user_detail_dict)
        print user_detail_json_str

        print type(json.loads(user_detail_json_str))
        # print(user_detail_json['_id'])
        # print user_detail_json
        # save_to_mongo(user_detail_dict)
        # save_to_es(user_detail_dict)
        # print(user_detail_dict)
        # print(user_detail_json)



# if __name__ == '__main__':
#     pool = Pool(processes=16)
#     for xx in pool.imap_unordered(zcool_user_info, range(1,10000)):
#         print xx
