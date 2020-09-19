import json
from pprint import pprint

import requests


def flatten_json(json_data):
    temp_dict = {}

    def loop_dict(dictionary, key_val=''):
        for key, value in dictionary.items():
            key = key.replace('_', '').replace('-', '').replace(' ', '').replace('.', '').replace(':', '')
            key = key.capitalize()
            # if key_val != '':
            #     key = key_val.capitalize() + key.capitalize()
            if key == 'Whois':
                whois_dict = {}
                whois_data = value.split('\n')
                for ind in whois_data:
                    data = ind.split(':')
                    if len(data) > 1:
                        whois_dict[data[0]] = data[1].strip()
                loop_dict(whois_dict, key)
            if type(value) is list:
                if len(value) > 0:
                    if type(value[0]) is dict:
                        for ind in value:
                            loop_dict(ind, key)
                    else:
                        if type(value) is list:
                            if len(value) > 1:
                                temp_dict['$VT'+key] = ' '.join(value[0:])
                            elif len(value) < 0:
                                pass
                            else:
                                temp_dict['$VT' + key] = str(value[0])

            elif type(value) is dict:
                if key in ('Lastanalysisresults', 'Lastanalysisstats', 'Totalvotes', 'Lasthttpresponseheaders'):
                    pass
                else:
                    loop_dict(value, key)
            else:
                if key == 'Whois':
                    pass
                else:
                    temp_dict['$VT'+key] = value

        return temp_dict

    f_data = loop_dict(json_data)
    return f_data


def get_ip_report(inward_array, var_array):
    check_ip_address_api = 'https://www.virustotal.com/api/v3/ip_addresses'
    flat_data = {}
    header = {'x-apikey': '3d0be0595a00dc2c9e4105f818aa54cc9f4e02de8fd7178b651767e4a73b9b4a'}
    for i in inward_array:
        if var_array[0] in i:
            try:
                response = requests.get(check_ip_address_api + '/' + i[var_array[0]], headers=header)
                ip_data = json.loads(response.content)
                flat_data = flatten_json(ip_data['data'])
                pprint(ip_data)
            except Exception as e:
                print('Error: {}'.format(e))
            try:
                for key, value in flat_data.items():
                    i[key] = value
            except Exception:
                pass
    # pprint(inward_array)
    pprint(flat_data)

ip_in_array = [{'$SrcIp': '114.104.158.172'}, {'$SrcIp': '201.18.18.173'}]
ip_v_array = ['$SrcIp']


get_ip_report(ip_in_array, ip_v_array)