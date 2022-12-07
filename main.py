import re
import json
from cmd_args import *
from datetime import datetime

for log in log_files:
    http_methods = {'GET': 0, 'POST': 0, 'HEAD': 0, 'PUT': 0, 'OPTIONS': 0,
                       'PATCH': 0, 'DELETE': 0, 'TRACE': 0, 'CONNECT': 0}
    top_ip = {}
    long_req = []


    def parsing_logs(line):
        ip_address = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group(0)
        date_time = re.search(r'\d{1,2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s.\d{4}', line).group(0)
        http_method = [i for i in http_methods.keys() if i in line][0]
        if re.search(r'https?:[/a-zа-яA-ZА-Я0-9\.\?\=\&\-\_]*', line):
            url = re.search(r'https?:[/a-zа-яA-ZА-Я0-9\.\?\=\&\-\_]*', line).group(0)
        else:
            url = 'n/a'
        length = int(line.rstrip().split()[-1])

        return [ip_address, date_time, http_method, url, length]


    def add_to(parsed_line):
        http_methods[parsed_line[2]] += 1
        if parsed_line[0] in top_ip.keys():
            top_ip[parsed_line[0]] += 1
        else:
            top_ip[parsed_line[0]] = 1
        long_req.append(parsed_line)
        long_req.sort(key=lambda x: x[-1], reverse=True)
        if len(long_req) > 3:
            long_req.pop()


    def long_reqs_to_dict(list_info):
        new_dict = dict()
        count = 1
        for item in list_info:
            my_dict = dict()
            my_dict["HTTP Meth"] = item[2]
            my_dict["URL"] = item[3]
            my_dict["IP"] = item[0]
            my_dict['Duration'] = item[4]
            my_dict['Date&Time'] = item[1]
            new_dict[count] = my_dict
            count += 1
        return new_dict


    with open(log, "r") as log_f:
        for line in log_f:
            parsed = parsing_logs(line)
            add_to(parsed)

    top_3_ip = sorted(top_ip.items(), key=lambda x: x[1], reverse=True)[:3]
    total_reqs = sum(http_methods.values())
    results = dict()
    results["Total Requests:"] = total_reqs
    results["HTTP Requests"] = http_methods
    results["Top-3 Longest Requests:"] = long_reqs_to_dict(long_req)
    results["Top-3 ip-addresses:"] = dict(top_3_ip)

    print(f"'******** File Name: {log} ********")
    print(json.dumps(results, indent=4))
    print()

    with open(f'{dir_for_parsed_files}parsed_logs_by_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")}.json',
              "w") as res_file:
        json.dump(results, res_file, indent=4)