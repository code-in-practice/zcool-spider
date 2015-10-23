
#coding=utf-8
import requests
from bs4 import BeautifulSoup

import json

def main_user(user_id, p):
    url = 'http://www.zcool.com.cn/u/' + str(user_id) + '/zcooler_recommend.xhtml?p=' + str(p)
    r = requests.get(url)
    bodydom = r.content

    bodysoup = BeautifulSoup(bodydom, 'html.parser')

    user_detail_dict = {}


    page_this = bodysoup.find(attrs= {'class': 'selected', 'btnmode': 'true'}).text.strip()
    print page_this
    page_total = bodysoup.find(attrs= {'class': 'pageNext', 'btnmode': 'true'}).previous_sibling.previous_sibling.text.strip()
    print page_total
    page_next = int(page_this) + 1
    if not page_next > page_total:
        main_user(user_id, page_next)

main_user(1, 1)