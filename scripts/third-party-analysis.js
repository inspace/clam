const puppeteer = require('puppeteer');
const fs = require('fs');

const flags = require('minimist')(process.argv.slice(2));
const inputFile = flags['i'];
const topN = parseInt(flags['t']);

var urls = fs.readFileSync(inputFile).toString().toString().split("\n");
urls.pop();

(async () => {
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  var cnt = 1;

  for(let page_url of urls){
    if (cnt > topN){
        break;
    }
    console.log(cnt, page_url);
    cnt = cnt+1;
    try{
        page.on('request', request=> {
            var asset_url = new URL(request.url())
            var hostname = asset_url.hostname;
            //console.log(asset_url);
            console.log(hostname);
            // Write something to file:
            fs.appendFile('test_out', page_url+" "+hostname+"\n", (err) => {
                if (err) throw err;
            });
        });
        const response = await page.goto(page_url, {waitUntil:'domcontentloaded'});

    }
    catch (err){
       console.log(err);
    }
  }

  await browser.close();
})();
