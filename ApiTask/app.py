import json
from datetime import date, datetime
from pprint import pprint as pp

import requests

API_KEY = "3d0be0595a00dc2c9e4105f818aa54cc9f4e02de8fd7178b651767e4a73b9b4a"
CHECK_WEBSITE_API_URL = 'https://www.virustotal.com/vtapi/v2/url/report'
CHECK_FILE_SCAN_API_URL = 'https://www.virustotal.com/vtapi/v2/file/report'
CHECK_DOMAIN_API_URL = 'https://www.virustotal.com/vtapi/v2/domain/report'
CHECK_IP_ADDRESS_API_URL = 'https://www.virustotal.com/vtapi/v2/ip-address/report'


def flatten_json(nested_json):
    response_output = {}
    for key, value in nested_json.items():
        incr = 1
        inc = 1
        if type(value) is dict:
            for k, v in value.items():
                if type(v) is dict:
                    for ind, val in v.items():
                        if type(val) is dict:
                            for ins_key, ins_val in val.items():
                                if type(ins_val) is dict:
                                    for ins_new_key, ins_new_val in ins_val.items():
                                        response_output['$VT' + key.capitalize() + str(k).capitalize() + str(ind).capitalize() + str(ins_key).capitalize() + str(ins_new_key).capitalize()] = ins_new_val
                                else:
                                    response_output['$VT' + key.capitalize() + str(k).capitalize() + str(ind).capitalize() + str(ins_key).capitalize()] = ins_val
                                # if type(ins_val) is list:
                                #     for list_val in ins_val:
                                #         response_output['VT_' + key + '_' + k + '_' + ind + '_' + ins_key + '_' + str(inc)] = list_val
                                #         inc += 1
                        # elif type(val) is list:
                        #     for list_val in val:
                        #         response_output['VT_' + key + '_' + k + '_' + ind + '_' + str(inc)] = list_val
                        #         inc += 1
                        else:
                            response_output['$VT'+key.capitalize()+str(k).capitalize()+str(ind).capitalize()] = val
                else:
                    response_output['$VT'+key.capitalize()+str(k).capitalize()] = v
        # elif type(value) is list:
        #     for ind in value:
        #         if type(ind) is dict:
        #             for i_key, i_value in ind.items():
        #                 response_output['VT_' + key + '_' + i_key + '_' + str(incr)] = i_value
        #                 incr += 1
        #         elif type(ind) is list:
        #             for i in ind:
        #                 response_output['VT_'+key + str(inc)] = i
        #                 inc += 1
        #         elif type(ind) is str:
        #             if ind.find('\n') != -1:
        #                 new_val = dict(ind.split('\n'))
        #                 pp(new_val)
        #             response_output['VT_' + key] = ind
        #         elif type(ind) is int:
        #             response_output['VT_' + key] = ind
        #         else:
        #             response_output['VT_' + key] = ind
        elif type(value) is str:
            if value.find(': ') != -1:
                print(type(value))
                new_val = value.split('\n')
                final_dict = {}
                for ind in new_val:
                    final_val = ind.split(': ')
                    if len(final_val) > 1:
                        final_dict[final_val[0]] = final_val[1]
                    else:
                        final_dict[final_val[0]] = ''
                for i, j in final_dict.items():
                    response_output['$VT' + key.capitalize() + str(i).capitalize()] = j
            else:
                response_output['$VT' + key.capitalize()] = value
        elif type(value) is int:
            response_output['$VT' + key.capitalize()] = value
        else:
            response_output['$VT'+key.capitalize()] = value
    return response_output


def check_websites(site):
    params = {'apikey': API_KEY, 'resource': site}
    response = requests.get(CHECK_WEBSITE_API_URL, params=params)
    response_json = json.loads(response.content)
    with open('website_data.json','w') as file:
        json.dump(response_json, file)
    filtered_json=flatten_json(response_json)
    pp(filtered_json)


def check_file(file):
    params = {'apikey': API_KEY, 'resource': file}
    response = requests.get(CHECK_FILE_SCAN_API_URL, params=params)
    response_json = json.loads(response.content)
    flat_json = flatten_json(response_json)
    pp(flat_json)


def check_domain(domain):
    params = {'apikey': API_KEY, 'domain': domain}
    response = requests.get(CHECK_DOMAIN_API_URL, params=params)
    response_json = json.loads(response.content)
    pp(response_json)
    flat_json = {}
    # final_json = []
    # for keys, values in response_json.items():
    #     temp_json = {}
    #     if type(values) is not str:
    #         print('not str')
    #         # if type(values) is list:
    #         #     print('\tlist')
    #         #     for ind in values:
    #         #         if type(ind) is dict:
    #         #             print('\t\tnot list')
    #         #             for k, v in ind.items():
    #         #                 print('\t\t\t', k, ' : ', v)
    #         #         else:
    #         #             print('\t\t',type(ind))
    #         # else:
    #         #     print('\tnot list')
    #         #     print('\t\t', type(values))
    #     else:
    #         # temp_json[keys] = values
    #         final_json.append({keys: values})

    # pp(flat_json)
    # pp(final_json)

def check_ip_address(ip_address):
    params = {'apikey': API_KEY, 'ip': ip_address}
    response = requests.get(CHECK_IP_ADDRESS_API_URL, params=params)
    response_json = json.loads(response.content)
    flat_json = flatten_json(response_json)
    filtered_json = {}
    whois_time = datetime.fromtimestamp(response_json['whois_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    filtered_json['$VT_IpInfo'] = [response_json['as_owner'], response_json['asn'], response_json['country'],
                                   response_json['network'], whois_time]
    filtered_json['$VT_DetectedReferrerSamples'] = [value
                                                    for i in range(len(response_json['detected_referrer_samples']))
                                                    for value in response_json['detected_referrer_samples'][i].values()]
    value = response_json['whois']
    final_dict = {}
    if value.find(': ') != -1:
        print(type(value))
        new_val = value.split('\n')
        for ind in new_val:
            final_val = ind.split(': ')
            if len(final_val) > 1:
                final_dict[final_val[0]] = final_val[1]
            else:
                final_dict[final_val[0]] = ''
    # for key, value in
    pp(final_dict)
    # filtered_json['$VT_WhoIs'] = [val for value ]
    #     for i, j in final_dict.items():
    #         response_output['VT_' + key + '_' + i] = j
    # else:
    #     response_output['VT_' + key] = value
    # filtered_json['$VT_']
    # pp(filtered_json)
    # pp(response_json)
    # print(type(a))

# check_websites('http://www.dailystudy.org/')
# time.sleep(15)
# check_websites('https://www.truecaller.com/')
# time.sleep(15)
# check_file('9498FF82A64FF445398C8426ED63EA5B')
# time.sleep(15)
check_domain('textspeier.de')
# check_ip_address('114.104.158.172')
