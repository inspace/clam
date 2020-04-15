from flask import Flask, make_response, request
import json

app = Flask(__name__)

report_log = open('report.log.txt', 'at')

'''
Sample Headers:
HTTP/1.1 200 OK
< ...
< Report-To: {"group": "network-errors", "max_age": 2592000,
              "endpoints": [{"url": "https://example.com/upload-reports"}]}
< NEL: {"report_to": "network-errors", "max_age": 2592000}
'''

report_to_d = { 
                "group": "network-errors", 
                "max-age": 2592000, 
                "endpoints": 
                    [
                        {"url": "https://92a80c753c9ef473931d7d4356d42786.report-uri.com/a/d/g"} #free report-uri domain
                    ]
              }

nel_d = {
          "report_to": "network-errors", 
          "max_age": 2592000,
          "include_subdomains": True,
          "success_fraction": 1.0,
          "failure_fractio ": 1.0

        }

report_to_hdr = json.dumps(report_to_d)
nel_hdr = json.dumps(nel_d)

@app.route('/')
def index():
    resp = make_response('<html><body><h1>Test</h1></body></html>', 200)
    resp.headers['Report-To'] = report_to_hdr
    resp.headers['NEL'] = nel_hdr
    return resp


'''
Sample Report:
{
  "age": 0,
  "type": "network-error",
  "url": "https://www.example.com/",
  "body": {
    "sampling_fraction": 0.5,
    "referrer": "http://example.com/",
    "server_ip": "123.122.121.120",
    "protocol": "h2",
    "method": "GET",
    "status_code": 200,
    "elapsed_time": 823,
    "type": "http.protocol.error"
  }
}
'''

@app.route('/reports', methods=['POST'])
def reports():
    report = request.data

    #send somewhere
    report_log.write(report)
    report_log.write('\n')

    return make_response('Success', 200)


    



if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5551)
    except KeyboardInterrupt:
        report_log.close()
        exit()
