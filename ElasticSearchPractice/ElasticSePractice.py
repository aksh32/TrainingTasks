import json
import elasticsearch
import pprint

pp = pprint.PrettyPrinter(width=41, compact=True)

# Connect to elasticsearch
es_object = elasticsearch.Elasticsearch([{'host': '192.168.86.52', 'port': 9200}])
if es_object.ping():
    print("Connected!!!!!!")
else:
    print("Not Connected!! try again!!!!!!!!!!")

# Create an index
    # index settings
settings = {
    "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
    },
    "mappings": {
                "members": {
                    "properties": {
                        "id":{
                            "type": "integer"
                        },
                        "title": {
                            "type": "text"
                        },
                        "submitter": {
                            "type": "text"
                        },
                        "description": {
                            "type": "text"
                        },
                        "calories": {
                            "type": "integer"
                        }
                    }
                }
    }
}

# create index

index_val = input(str("Enter index name: "))
if not es_object.indices.exists(index_val):
    es_object.indices.create(index=index_val, body=settings)
    print("index created!!!")
else:
    print("not created!!!!!!!!!!!!!!!!!")

# insert into index
recipe = []
rec_id = int(input("Enter id: "))
title = input("Enter title of recipe: ")
submitter = input("Enter submitter: ")
description = input("Enter description: ")
calories = input("Enter calories: ")
recipe = {"title": title, "submitter": submitter, "description": description, "calories": calories}
es_object.index(index=index_val, id=rec_id, doc_type='members', body=recipe)


index_info = es_object.search(index=index_val, doc_type="members", body={"from": 0, "size": 100, "query": {"match_all": {}}})

for ind in range(len(index_info)):
    pp.pprint(index_info['hits']['hits'][ind]['_id'])
    pp.pprint(index_info['hits']['hits'][ind])
# , "size": "10"
# "from": "0",
