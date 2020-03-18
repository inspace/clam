#!/usr/bin/python
import sys
import fileinput
import json

# unfuck the httparchive format

for line in fileinput.input():
    line = line.strip()
    try:
        text = line.lower()
        chunks = text.split(',')

        page_id = chunks[1].replace("\"", "")
        url = chunks[5].replace("\"", "")

        report_index = text.index("report-to =")
        report_lbrace_index = text.index('{', report_index)
        report_rbrace_index1 = text.index('}', report_index)
        report_rbrace_index2 = text.index(']', report_rbrace_index1)
        report_rbrace_index3 = text.index('}', report_rbrace_index2)
        report_header_escaped = text[report_lbrace_index:report_rbrace_index3+1]
        report_header = report_header_escaped.replace("\\", "")
        report_header = report_header.replace("\'", "\"")   # JSON doesn't use single quotes
        report_header_obj = json.loads(report_header)

        nel_index = text.index("nel =")
        nel_lbrace_index = text.index('{', nel_index)
        nel_rbrace_index = text.index('}', nel_index)
        nel_header_escaped = text[nel_lbrace_index:nel_rbrace_index+1]
        nel_header = nel_header_escaped.replace("\\", "")
        nel_header = nel_header.replace("\'", "\"")
        nel_header_obj = json.loads(nel_header)

        nel_maxage = nel_header_obj[u'max_age']
        success_fraction = nel_header_obj[u'success_fraction'] if u'success_fraction' in nel_header_obj else 0 # default
        failure_fraction = nel_header_obj[u'failure_fraction'] if u'failure_fraction' in nel_header_obj else 1 # default

        report_maxage = report_header_obj[u'max_age']
        endpoints = report_header_obj[u'endpoints']       # parsing failures because this is missing
        endpoints_str = ','.join([x[u'url'] for x in endpoints])

        print('%s|%s|%s|%s|%s|%s|%s' % (page_id, url, nel_maxage, success_fraction, failure_fraction, report_maxage, endpoints_str))

    except Exception as e:
        #sys.stderr.write('%s, %s\n' % (nel_header, report_header))
        sys.stderr.write('%s\n' % e)
        sys.stderr.write('%s\n' % text)