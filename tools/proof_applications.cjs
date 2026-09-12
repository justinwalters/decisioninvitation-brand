const { chromium } = require('playwright');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const root = path.resolve(__dirname, '..');
const source = path.join(root, 'templates/applications');
const out = path.join(source, 'review');

const captures = [
  ['business-card.html', '.business-card', ['business-card-1.png', 'business-card-2.png']],
  ['letterhead.html', '.page', ['letterhead-1.png']],
  ['decision-brief.html', '.page', ['decision-brief-1.png', 'decision-brief-2.png']],
  ['presentation.html', '.slide', ['presentation-1.png', 'presentation-2.png', 'presentation-3.png', 'presentation-4.png']],
  ['product-moments.html', '.moment', ['product-moments-1.png', 'product-moments-2.png', 'product-moments-3.png', 'product-moments-4.png']],
  ['social-layouts.html', '.social-proof', ['social-layouts-1.png', 'social-layouts-2.png', 'social-layouts-3.png']],
];

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));

  async function open(file) {
    await page.goto(pathToFileURL(path.join(source, file)).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const broken = await page.locator('img').evaluateAll(images => images.filter(image => !image.complete || !image.naturalWidth).map(image => image.src));
    if (broken.length) errors.push(`${file}: broken images: ${broken.join(', ')}`);
  }

  await open('index.html');
  await page.screenshot({ path: path.join(out, 'index.png'), fullPage: true, animations: 'disabled' });

  for (const [file, selector, names] of captures) {
    await open(file);
    const items = page.locator(selector);
    if (await items.count() !== names.length) errors.push(`${file}: expected ${names.length} ${selector} elements`);
    for (let index = 0; index < names.length; index += 1) {
      await items.nth(index).screenshot({ path: path.join(out, names[index]), animations: 'disabled' });
    }
  }

  await open('email-signature.html');
  await page.locator('.signature-stage').screenshot({ path: path.join(out, 'email-signature.png'), animations: 'disabled' });

  await page.setViewportSize({ width: 390, height: 844 });
  for (const [file, name] of [
    ['index.html', 'index-mobile.png'],
    ['email-signature.html', 'email-signature-mobile.png'],
    ['product-moments.html', 'product-moments-mobile.png'],
  ]) {
    await open(file);
    await page.screenshot({ path: path.join(out, name), fullPage: true, animations: 'disabled' });
    const overflow = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth }));
    if (overflow.document > overflow.viewport) errors.push(`${file}: page-level horizontal overflow ${overflow.document}/${overflow.viewport}`);
  }

  await browser.close();
  console.log(JSON.stringify({ captures: 21, errors }, null, 2));
  if (errors.length) process.exitCode = 1;
})().catch(error => {
  console.error(error);
  process.exit(1);
});
