import base64
import json
import os
import yaml
from pprint import pprint
import requests


path = os.environ["WORKDIR"]
with open(path + "/lookup_plugins/virustotal1/dnifconfig.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


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


headers = {'x-apikey': cfg['lookup_plugin']['VT_API_KEY'], 'Accept': 'application/json'}


def get_url_report(inward_array, var_array):
    check_url_api = "https://www.virustotal.com/api/v3/urls"
    flat_data = {}
    for i in inward_array:
        if var_array[0] in i:
            try:
                encoded_url = base64.b64encode(i[var_array[0]].encode())
                res = requests.get(check_url_api + '/' + encoded_url.decode().replace('=', ''), headers=headers)
                url_data = json.loads(res.content)
                flat_data = flatten_json(url_data)
            except Exception as e:
                print('Error: {}'.format(e))
            try:
                for key, value in flat_data.items():
                    i[key] = value
            except Exception:
                pass
    return inward_array


def get_domain_report(inward_array, var_array):
    check_domain_api = 'https://www.virustotal.com/api/v3/domains'
    flat_data = {}
    for i in inward_array:
        if var_array[0] in i:
            try:
                response = requests.get(check_domain_api + '/' + i[var_array[0]], headers=headers)
                domain_data = json.loads(response.content)
                flat_data = flatten_json(domain_data['data'])
            except Exception as e:
                print('Error: {}'.format(e))
            try:
                for key, value in flat_data.items():
                    i[key] = value
            except Exception:
                pass
    return inward_array


def get_ip_report(inward_array, var_array):
    check_ip_address_api = 'https://www.virustotal.com/api/v3/ip_addresses'
    flat_data = {}
    for i in inward_array:
        if var_array[0] in i:
            try:
                response = requests.get(check_ip_address_api + '/' + i[var_array[0]], headers=headers)
                ip_data = json.loads(response.content)
                flat_data = flatten_json(ip_data['data'])
            except Exception as e:
                print('Error: {}'.format(e))
            try:
                for key, value in flat_data.items():
                    i[key] = value
            except Exception:
                pass
    return inward_array


# url_in_array = [{'$SrcUrl': 'https://www.truecaller.com/'}, {'$SrcUrl': 'http://www.dailystudy.org/'}]
# url_v_array = ['$SrcUrl']
#
# domain_in_array = [{'$SrcDomain': 'textspeier.de'}, {'$SrcDomain': 'photoscape.ch/Setup.exe'}]
# domain_v_array = ['$SrcDomain']
#
# ip_in_array = [{'$SrcIp': '114.104.158.172'}, {'$SrcIp': '201.18.18.173'}]
# ip_v_array = ['$SrcIp']


# pprint(get_url_report(url_in_array, url_v_array))
# print('\n*******************************************************************************\n')
# pprint(get_domain_report(domain_in_array, domain_v_array))
# print('\n*******************************************************************************\n')
# pprint(get_ip_report(ip_in_array, ip_v_array))

