const {saveItem} = require('crawlab-sdk')
const puppeteer = require('puppeteer');

async function parse(page) {
    console.log(`parsing ${page.url()}`);

    // Wait for the results page to load and display the results.
    const resultsSelector = '.newsList > li';
    await page.waitForSelector(resultsSelector);

    // Extract the results from the page.
    const items = await page.evaluate(resultsSelector => {
        return [...document.querySelectorAll(resultsSelector)].map(anchor => {
            const title = anchor.querySelector('.titleBar a') ? anchor.querySelector('.titleBar a').innerText : '';
            const url = anchor.querySelector('.titleBar a') ? anchor.querySelector('.titleBar a').getAttribute('href') : '';
            const img_url = anchor.querySelector('.newsList-img img') ? anchor.querySelector('.newsList-img img').getAttribute('src') : '';
            const abstract = anchor.querySelector('.newsDigest p') ? anchor.querySelector('.newsDigest p').innerText : '';
            return {
                title, url, img_url, abstract,
            };
        });
    }, resultsSelector);

    // Print all the files.
    for (let item of items) {
        // console.log(item);
        await saveItem(item);
    }
}

async function run() {
    // browser
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    // page
    const page = await browser.newPage();

    // start page
    await page.goto('https://tech.163.com/internet/');

    while (true) {
        // parse page
        await parse(page);

        // next page
        const res = await page.evaluate(() => document.querySelector('a.pages_flip:last-child'));

        if (res) {
            // go to next page
            await page.click('a.pages_flip:last-child');
            await new Promise(resolve => setTimeout(resolve, 5000));
        } else {
            // last page
            break;
        }
    }

    await browser.close();
}

run()
