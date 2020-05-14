import fileinput
import sys
import csv
import json

for line in  csv.reader(fileinput.input(), quotechar='"', delimiter=' '):
    client_ip = line[0]
    nel_report_utf = line[11]
    nel_report = nel_report_utf.decode('string_escape')
    # nel_report_utf.encode('utf8').decode('unicode_escape') # for python3
    rtt = int(line[12])

    print('%s %d %s' % (client_ip, rtt, nel_report))