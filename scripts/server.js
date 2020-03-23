const http = require('http');
const fs = require('fs');

const port = 80;
const reportToHost1 = "https://neltest.azurefd.net/report";
const reportToHost2 = "https://555f34ef0a29c5fac9a9b61e98f3586a.report-uri.com/a/d/g";
const nelHeader = { report_to: "default", max_age: 10, include_subdomains: true, success_fraction: 1.0 };
const reportToHeader = { group: "default", max_age: 10, endpoints: [ {url: reportToHost1}, {url: reportToHost2} ] };

const requestHandler = (request, response) => {
        url = request.url;
        if(url !== "/"){
                console.log(url);
        }

        if(url.startsWith('/report') && request.method === "POST") {
                console.log(new Date().toLocaleString() + " Got Report");

                var body = "";
                request.on('data', function(data){
                        body += data;
                })

                request.on('end', function() {
                        console.log("Report");
                        console.log(body);

                        response.statusCode = 410;
                        //response.statusMessage = '';
                        //response.writeHead(301, {Location: reportToHost2});
                        response.end();
                })
        } else {
                response.setHeader("NEL", JSON.stringify(nelHeader));
                response.setHeader("Report-To", JSON.stringify(reportToHeader));

                fs.readFile("17k.gif", function(error, content) {
                        response.writeHead(200, { 'Content-Type': 'image/gif' });
                        response.end(content, 'utf-8');
                });
        }
}

const server = http.createServer(requestHandler)

server.listen(port, (err) => {
        if (err) {
                return console.log('something bad happened', err);
        }

        console.log(`server is listening on ${port}`);
})
