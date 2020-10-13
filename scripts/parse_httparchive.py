#!/usr/bin/python
import sys
import fileinput
import json
import yaml
import traceback

# unfuck the httparchive format
# could have used this instead https://github.com/torfsen/barely_json

output_format = '|'.join(['%s']*8)

def parse_nel_header(text):
    error_list = []
    nel_index = text.index("nel =")

    try:
        nel_lbrace_index = text.index('{', nel_index)
    except:
        return "empty nel header", {}  # empty header

    nel_rbrace_index = text.index('}', nel_index)
    nel_header_escaped = text[nel_lbrace_index:nel_rbrace_index+1]
    nel_header = nel_header_escaped.replace("\\", "")

    if ";" in nel_header and ":" not in nel_header:
        nel_header = nel_header.replace(";", ":")   # JSON doesn't parse single quotes
        error_list.append('semi-colon fields in nel header')

    try:
        nel_header_obj = json.loads(nel_header)
    except:
        nel_header_obj = yaml.safe_load(nel_header) # try parsing as YAML instead https://stackoverflow.com/questions/31029320/fix-unquoted-keys-in-json-like-file-so-that-it-uses-correct-json-syntax

        if 'report_to' not in nel_header_obj:
            nel_header = nel_header.replace('report_to:', 'report_to: ') \
                                   .replace('max_age:', 'max_age: ') \
                                   .replace('include_subdomains:', 'include_subdomains: ') \
                                   .replace('success_fraction:', 'success_fraction: ') \
                                   .replace('failure_fraction:', 'failure_fraction: ')

            nel_header_obj = yaml.safe_load(nel_header)
            error_list.append('no space after colon in nel')

        # if it worked try figuring out what was wrong
        if "\'" in nel_header:
            error_list.append("single quotes in nel header")
        elif "\"" not in nel_header:
            error_list.append("unquoted keys in nel header")
        else:
            error_list.append("unknown error fixed with yaml")

    error = ",".join(error_list)

    return error, nel_header_obj

def parse_report_headers(text):
    # TODO Deal with multiple Report-To headers

    error_list = []

    try:
        report_index = text.index("report-to =")
    except:
        return "no report header", {}

    try:
        report_lbrace_index = text.index('{', report_index)
    except:
        return "empty report header", {}

    report_rbrace_index1 = text.index('}', report_index)

    try:
        report_rbrace_index2 = text.index(']', report_rbrace_index1) # missing endpoints list
    except:
        report_rbrace_index2 = report_rbrace_index1
        error_list.append('missing endpoints')

    report_rbrace_index3 = text.index('}', report_rbrace_index2)
    report_header_escaped = text[report_lbrace_index:report_rbrace_index3+1]
    report_header = report_header_escaped.replace("\\", "")

    if ";" in report_header and "," not in report_header:
        report_header = report_header.replace(";", ",")
        error_list.append('semi-colon fields in report header')

    try:
        report_header_obj = json.loads(report_header)
    except:
        report_header_obj = yaml.safe_load(report_header) # try fixing with yaml
        
        # check if keys got messed up because of no space after colon
        # assume all properties have the same issue
        if 'group' not in report_header_obj:
            report_header = report_header.replace('group:', 'group: ') \
                                         .replace('max_age:', 'max_age: ') \
                                         .replace('endpoints:', 'endpoints: ') \
                                         .replace('url:', 'url: ') \
                                         .replace('include_subdomains:', 'include_subdomains: ')
            report_header_obj = yaml.safe_load(report_header)
            error_list.append('no space after colon in report')

        # if it worked try figuring out what was wrong
        if "\'" in report_header:
            error_list.append("single quotes in report header")
        elif "\"" not in report_header:
            error_list.append("unquoted keys in report header")
        else:
            error_list.append("unknown error fixed with yaml")

    errors = ",".join(error_list)

    return errors,report_header_obj

def format_errors(nel_errors, report_errors):
    # lol
    errors = ""

    if nel_errors:
        errors += nel_errors

    if report_errors:
        if not errors:
            errors = report_errors
        else:
            errors += "," + report_errors

    return errors

if __name__ == '__main__':

    for line in fileinput.input():
        line = line.strip()
        try:
            text = line.lower()
            chunks = text.split(',')

            page_id = chunks[1].replace("\"", "")
            url = chunks[5].replace("\"", "")

            nel_errors, nel_header_obj = parse_nel_header(text)
            report_errors, report_header_obj = parse_report_headers(text)

            nel_maxage = nel_header_obj.get(u'max_age', -1)
            success_fraction = nel_header_obj.get(u'success_fraction', 0) # if u'success_fraction' in nel_header_obj else 0 # default
            failure_fraction = nel_header_obj.get(u'failure_fraction', 1) # if u'failure_fraction' in nel_header_obj else 1 # default

            report_maxage = report_header_obj.get(u'max_age', -1)
            endpoints = report_header_obj.get(u'endpoints', [])       # parsing failures because this is missing
            endpoints_str = ','.join([x[u'url'] for x in endpoints])

            errors = format_errors(nel_errors, report_errors)

            print(output_format % (page_id, url, nel_maxage, success_fraction, failure_fraction, report_maxage, endpoints_str, errors))

        except Exception as e:
            track = traceback.format_exc()
            sys.stderr.write(track)
            sys.stderr.write('%s\n' % text)
