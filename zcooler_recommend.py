
#coding=utf-8
import requests
from bs4 import BeautifulSoup

import json

def main_user(user_id, p):
    url = 'http://www.zcool.com.cn/u/' + str(user_id) + '/zcooler_recommend.xhtml?p=' + str(p)
    r = requests.get(url)
    bodysoup = BeautifulSoup(r.content, 'html.parser')

    if(bodysoup.find_all(attrs={'class': 'camLiCon'}).__len__() > 0):
        for w in bodysoup.find_all(attrs={'class': 'camLiCon'}):
            print w.previous_sibling.previous_sibling['href']

    page_this = bodysoup.find(attrs= {'class': 'selected', 'btnmode': 'true'}).text.strip()
    print 'user_id: ' + str(user_id) + ' page_this: ' + str(page_this)
    page_total = bodysoup.find(attrs= {'class': 'pageNext', 'btnmode': 'true'}).previous_sibling.previous_sibling.text.strip()
    print 'user_id: ' + str(user_id) + ' page_total: ' + str(page_total)
    page_next = int(page_this) + 1
    if not page_next > int(page_total):
        main_user(user_id, page_next)


for i in xrange(1, 1000):
    main_user(i, 1)
