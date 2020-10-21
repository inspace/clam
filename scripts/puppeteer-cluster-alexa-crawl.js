// Install puppeteer-cluster using "npm install --save puppeteer-cluster"
// Run using "node puppeteer-cluster.js <alexa.csv>"

const { Cluster } = require('puppeteer-cluster');

const fs = require('fs').promises;

(async () => {
    const cluster = await Cluster.launch({
        concurrency: Cluster.CONCURRENCY_CONTEXT,
        maxConcurrency: 5,
        monitor: true,
    });

    await cluster.task(async ({ page, data: url }) => {
        //console.log(url);
        page.on('request', request=> {
            var asset_url = new URL(request.url())
            var hostname = asset_url.hostname;
            console.log(url +" " +asset_url+" "+hostname);
         })
        await page.goto(url, { waitUntil: 'domcontentloaded' });
        const pageTitle = await page.evaluate(() => document.title);
        console.log(`Page title of ${url} is ${pageTitle}`);
    });

    // In case of problems, log them
    cluster.on('taskerror', (err, data) => {
        console.log(`  Error crawling ${data}: ${err.message}`);
    });

    // Read the alexa top N .csv file from the current directory
    const csvFile = await fs.readFile(__dirname + '/top10.csv', 'utf8');
    const lines = csvFile.split('\n');
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const splitterIndex = line.indexOf(',');
        if (splitterIndex !== -1) {
            const domain = line.substr(splitterIndex + 1);
            // queue the domain
            cluster.queue('http://www.' + domain);
        }
    }

    await cluster.idle();
    await cluster.close();
})();
