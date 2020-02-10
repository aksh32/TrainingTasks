import csv
import pprint

import redis

csv_file_path = 'InputData/test.csv'

with open(csv_file_path, 'r') as csv_file:
    csv_data = csv.reader(csv_file)
    for rows in csv_data:
        # pp.pprint(rows)
        rows = [x.strip() for x in rows]
        rows = [x.replace(' ', '') for x in rows]
        rows = [x.strip("'") for x in rows]
        rows = [x.strip('"') for x in rows]

    csv_final_data = {}
    for row in rows:
        clean_data = str(row).split('/')
        if len(clean_data) <= 1:
            pass
        elif len(clean_data) > 2:
            csv_final_data[clean_data[1]] = clean_data[0]
        else:
            csv_final_data[clean_data[1]]= clean_data[0]

redis_conn = redis.Redis(charset="utf-8", decode_responses=True)
hash_set_name = 'country_data'
if redis_conn:
    print("connected!!!!!!")
for key, value in csv_final_data.items():
    # redis_conn.set(key, value)
    # redis_conn.incr(value+"_count")
    redis_conn.hset(hash_set_name, key, value)
    redis_conn.hincrby(hash_set_name, 1)

pprint.pprint(redis_conn.hgetall(hash_set_name))
# print('\n------------state and country data------------\n')

# with open('./OutputData/redis_data.txt', 'a+') as outputfile:
#     for key in redis_conn.scan_iter():
#         key = key.decode('utf-8')
#         if str(key).find("_count") == -1:
#             # print('{state: '+key+', country: '+redis_conn.get(key).decode('utf-8')+'}')
#             outputfile.write('{state: '+key+', country: '+redis_conn.get(key).decode('utf-8')+'}\n')
# print("state and country data inserted successfully!!!!!!!!!!")
#
# # print('\n------------count of data------------\n')
# with open('./OutputData/redis_data_count.txt', 'a+') as countOpFile:
#     for count_key in redis_conn.scan_iter(match='*_count'):
#         count_key = count_key.decode('utf-8')
#         # print('{country: '+count_key+', count: '+redis_conn.get(count_key).decode('utf-8')+'}')
#         countOpFile.write('{country: '+count_key+', count: '+redis_conn.get(count_key).decode('utf-8')+'}\n')
# print("country and count data inserted successfully!!!!!!!!!!")

for count_key in redis_conn.scan_iter(match=''):
        count_key = count_key.decode('utf-8')
        # print('{country: '+count_key+', count: '+redis_conn.get(count_key).decode('utf-8')+'}')
        countOpFile.write('{country: '+count_key+', count: '+redis_conn.get(count_key).decode('utf-8')+'}\n')

