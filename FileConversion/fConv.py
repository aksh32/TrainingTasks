import csv
import json
import pprint
import time

import elasticsearch

pp = pprint.PrettyPrinter(width=41, compact=True)


class ConvertFile:
    def getcsvfile(self, csv_file_path):
        csv_final_data = dict()
        with open(csv_file_path, 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            for rows in csv_data:
                # pp.pprint(rows)
                rows = [x.strip() for x in rows]
                rows = [x.replace(' ', '') for x in rows]
                rows = [x.strip("'") for x in rows]
                rows = [x.strip('"') for x in rows]
                # rows = [x.replace('o', "0") for x in rows]

            print("-------------------------------------------------------")
            # pp.pprint(rows)

            for row in rows:
                clean_data = str(row).split('/')
                if len(clean_data) <= 1:
                    csv_final_data[clean_data[0]] = " "
                else:
                    if clean_data[0] not in csv_final_data:
                        csv_final_data[clean_data[0]] = []

                    for item in clean_data[1:]:
                        csv_final_data[clean_data[0]].append(item)

            return csv_final_data

    def convertFileToJson(self, csvoutput):
        with open('csv_export.json', 'w') as outputFile:
            json.dump(csvoutput, outputFile)

    def store_data_to_elasticsearch(self, input_data):
        # elasticsearch
        es_obj = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es_obj.ping:
            print("Connected to localhost!!")
        else:
            print("Connection Failed to localhost!!! try again!!!!!!!!")

        # create index
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "members": {
                    "properties": {
                        "country_name": {
                            "type": "text"
                        },
                        "city": {
                            "type": "text"
                        },
                        "count": {
                            "type": "integer"
                        }
                    }
                }
            }
        }

        index_name = "country"
        # create index
        if not es_obj.indices.exists(index_name):
            es_obj.indices.create(index=index_name, body=settings)
            print("index created!!")

        print("inserting data")
        index_ids = []
        json_dump = {}
        flag = False
        upd_flag = False
        tmp = es_obj.search(index=index_name, doc_type="members", body={"query": {"match_all": {}}})
        hit = tmp['hits']['total']
        # index is empty
        if hit == 0:
            pass
        else:
            index_info = es_obj.search(index=index_name, doc_type="members",
                                       body={"from": 0, "size": 64, "query": {"match_all": {}}})

            for ind in range(index_info['hits']['total']):
                index_ids.append(index_info['hits']['hits'][ind]['_id'])
            upd_flag = True

        i = 0
        for key, value in input_data.items():
            if len(value) >= 1:
                for ind in value:
                    count_o = ind.lower().count('o')
                    if count_o >= 2:
                        # Data exists
                        if upd_flag:
                            key_o = key
                            key = key.replace('o', '0')

                            val_o = ind
                            ind = ind.replace('o', '0')
                            count_0 = ind.lower().count('0')
                            if count_0 >= 2:
                                ind_id = index_ids[i]
                                # update data
                                es_obj.index(index=index_name, doc_type="members", id=ind_id,
                                             body={"og_country_name": key_o, "updated_country_name": key,
                                                   "og_city": val_o, "updated_city": ind, "count_'o'": count_o,
                                                   "count_'0'": count_0})
                            if i <= len(index_ids):
                                i += 1
                        else:
                            # insert data
                            es_obj.index(index=index_name, doc_type="members", body={"og_country_name": key,
                                                                                     "og_city": ind,
                                                                                     "count_'o'": count_o})
                    else:
                        json_dump[key] = ind
            flag = True

        if flag:
            print("data Inserted...")

        self.convertFileToJson(json_dump)




c1 = ConvertFile()
fPath = "test.csv"
output = c1.getcsvfile(fPath)
c1.store_data_to_elasticsearch(output)
