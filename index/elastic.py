#coding=utf-8
__author__ = 'smile'

from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()

result = es.index(index="zcool", doc_type="user", id=1, body={"any": "data", "timestamp": datetime.now()})
# print result

user = es.get(index="zcool", doc_type="user", id=1)
u = es.search(index='zcool', doc_type='user')['hits']['hits'][0]['_source']
print user
print u

curl -XGET 'http://localhost:9200/zcool/user/_search?pretty' -d '{
    "query": {
        "filtered" : {
            "query" : {
                "query_string" : {
                    "query" : "明"
                }
            }
        }
    }
}
'
