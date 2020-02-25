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
                                        response_output['VT_' + key + '_' + k + '_' + ind + '_' + ins_key + '_' + ins_new_key] = ins_new_val
                                else:
                                    response_output['VT_' + key + '_' + k + '_' + ind + '_' + ins_key] = ins_val
                                # if type(ins_val) is list:
                                #     for list_val in ins_val:
                                #         response_output['VT_' + key + '_' + k + '_' + ind + '_' + ins_key + '_' + str(inc)] = list_val
                                #         inc += 1
                        # elif type(val) is list:
                        #     for list_val in val:
                        #         response_output['VT_' + key + '_' + k + '_' + ind + '_' + str(inc)] = list_val
                        #         inc += 1
                        else:
                            response_output['VT_'+key+'_'+k+'_'+ind] = val
                else:
                    response_output['VT_'+key+'_'+k] = v
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
                    response_output['VT_' + key + '_' + i] = j
            else:
                response_output['VT_' + key] = value
        elif type(value) is int:
            response_output['VT_' + key] = value
        else:
            response_output['VT_'+key] = value
    return response_output


def check_websites(site):
    params = {'apikey': API_KEY, 'resource': site}
    response = requests.get(CHECK_WEBSITE_API_URL, params=params)
    response_json = json.loads(response.content)
    filtered_json = {}
    malicious_found = []
    not_malicious = []
    filtered_json = {'$VTFileScanId': response_json['filescan_id'],
                     '$VTPermaLink': response_json['permalink'],
                     '$VTResource': response_json['resource'],
                     '$VTScanDate': response_json['scan_date'],
                     '$VTScanId': response_json['scan_id'],
                     '$VTTotal': response_json['total'],
                     '$VTUrl': response_json['url'],
                     '$VTVerboseMsg': response_json['verbose_msg']}
    for key,value in response_json['scans'].items():
        print('in for')
        for ins_key, ins_val in value.items():
            print('ins_key: {} | ins_val: {}'.format(ins_key, ins_val))
            filtered_json['$VTScanData'] = key
            if ins_key == 'detected':
                print('in if')
                filtered_json['$VTDetected'] = ins_val
            if ins_key == 'result':
                print('in 2nd if')
                filtered_json['$VTResult'] = ins_val
    # for key, value in response_json['scans'].items():
    #     data_list = [response_json['filescan_id'], response_json['positives'],
    #                                         response_json['scan_id'], response_json['scan_date'],
    #                                         response_json['response_code'], response_json['verbose_msg']]
    #     filtered_json['$VT_ScanInfo'] = data_list
    #     if value['detected']:
    #         malicious_found.append([key, value['detected'], value['result']])
    #     else:
    #         not_malicious.append([key, value['detected'], value['result']])
    #     filtered_json['$VT_NotMalicious'] = not_malicious
    #     filtered_json['$VT_Malicious'] = malicious_found
    pp(filtered_json)
    # pp(response_json)


def check_file(file):
    params = {'apikey': API_KEY, 'resource': file}
    response = requests.get(CHECK_FILE_SCAN_API_URL, params=params)
    response_json = json.loads(response.content)
    not_malicious = []
    malicious_found = []
    filtered_json = {}
    for key, value in response_json['scans'].items():
        # print(key, value)
        data_list = [key, response_json['permalink'], response_json['resource'],
                     response_json['positives'], response_json['scan_id'], response_json['verbose_msg']]
        filtered_json['$VT_ScanInfo'] = data_list
        if value['detected']:
            malicious_found.append([key, value['detected'], value['result'], value['version']])
        else:
            not_malicious.append([key, value['detected'], value['result'], value['version']])
        filtered_json['$VT_MaliciousUrlInfo']=malicious_found
        filtered_json['$VT_FoundNotMalicious']=not_malicious
    # pp(filtered_json)
    flat_json = flatten_json(filtered_json)
    pp(flat_json)
    # pp(response_json)


def check_domain(domain):
    params = {'apikey': API_KEY, 'domain': domain}
    response = requests.get(CHECK_DOMAIN_API_URL, params=params)
    response_json = json.loads(response.content)
    # pp(response.json())
    filtered_json = {}
    detected_urls = [[response_json['detected_urls'][i]['positives'], response_json['detected_urls'][i]['scan_date'],
                      response_json['detected_urls'][i]['url']] for i in range(len(response_json['detected_urls']))]
    # domain_info = [value for value in response_json['Webutation domain info'].values()]
    # popularity_ranks = [val for key, value in response_json['popularity_ranks'].items() for val in value.values()]
    dns_records = [[response_json['dns_records'][i]['ttl'], response_json['dns_records'][i]['type'],
                    response_json['dns_records'][i]['value']] for i in range(len(response_json['dns_records']))]
    dns_date = datetime.fromtimestamp(response_json['dns_records_date']).strftime('%Y-%m-%d %H:%M:%S')
    # undetected_urls = [value for value in response_json['undetected_urls'] for i in range(len(value))]
    whois_time = datetime.fromtimestamp(int(response_json['whois_timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
    filtered_json['$VT_Info'] = [response_json['subdomains'], dns_date, whois_time, response_json['whois_timestamp']]
    filtered_json['$VT_DetectedUrls'] = detected_urls
    filtered_json['$VT_DomainInfo'] = [value for value in response_json['Webutation domain info'].values()]
    filtered_json['$VT_PopularityRank'] = [val for key, value in response_json['popularity_ranks'].items() for val in value.values()]
    filtered_json['$VT_DnsRecords'] = dns_records
    filtered_json['$VT_UndetectedUrls'] = [value for value in response_json['undetected_urls'] for i in range(len(value))]
    # pp(response_json['whois'])
    # pp(response_json)
    flat_json = flatten_json(response_json)
    pp(flat_json)
    # pp(whois)


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
check_websites('https://www.truecaller.com/')
# time.sleep(15)
# check_file('9498FF82A64FF445398C8426ED63EA5B')
# time.sleep(15)
# check_domain('textspeier.de')
# check_ip_address('114.104.158.172')
