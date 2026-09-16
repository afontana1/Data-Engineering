// https://www.browserless.io/blog/2022/08/26/zillow-scraper/

const options = {
    // the chromium revision to use
    // default is puppeteer.PUPPETEER_REVISIONS.chromium
    revision: '',

    // additional path to detect local chromium copy (separate with a comma if multiple paths)
    detectionPath: '',

    // custom path to download chromium to local, require dir permission: 0o777
    // default is user home dir
    downloadPath: '',

    // the folder name for chromium snapshots (maybe there are multiple versions)
    folderName: '.chromium-browser-snapshots',

    // the stats file name, cache stats info for latest installation
    statsName: '.pcr-stats.json',

    // default hosts are ['https://storage.googleapis.com', 'https://npmmirror.com/mirrors']
    hosts: [],

    cacheRevisions: 2,
    retry: 3,
    silent: false
};

(async () => {

    const PCR = require("puppeteer-chromium-resolver");
    const options = {};
    const stats = await PCR(options);
    const browser = await stats.puppeteer.launch({
        headless: false,
        args: ["--no-sandbox"],
        executablePath: stats.executablePath,
    }).catch(function(error) {
        console.log(error);
    });
    const page = await browser.newPage();
    await page.goto("https://www.zillow.com/");
    //await browser.close();
    //await page.setViewport({width: 1080, height: 1024});

})();