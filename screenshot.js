const puppeteer = require('puppeteer');

(async () => {
  const url = process.argv[2];
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });
  await page.setViewport({ width: 1200, height: 800 });
  await page.screenshot({ path: 'screenshot.png' });
  await browser.close();
})();
