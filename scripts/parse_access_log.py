#!/usr/bin/python
import fileinput
import sys
import csv
import json

for line in  csv.reader(fileinput.input(), quotechar='"', delimiter=' '):
    try:
        nel_report_utf = line[11]
        if nel_report_utf == '-':
            continue # not a nel upload

        client_ip = line[0]
        datetime_str_fucked = line[3]
        datetime_str = datetime_str_fucked.strip('[')

        nel_report_str = nel_report_utf.decode('string_escape')
        # nel_report_utf.encode('utf8').decode('unicode_escape') # for python3
        rtt = int(line[12]) / 1000
        region = line[-1]

        #print(nel_report_str)

        nel_reports = json.loads(nel_report_str)
        for nel_report in nel_reports:
            age = nel_report['age'] / 1000
            fetch_time = nel_report['body']['elapsed_time']
            #server_ip = nel_report['body']['server_ip']
            url = nel_report['url']

            print('%s %s %s %d %d %d %s' % (region, datetime_str, client_ip, rtt, fetch_time, age, url))
    except:
        sys.stderr.write('Skipping line: %s\n' % line)