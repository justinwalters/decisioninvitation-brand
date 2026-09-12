const { test } = require('node:test');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const url = process.env.BRAND_URL || 'http://127.0.0.1:3000/brand';
test('brand center controls change previews, filter downloads and preserve a mobile reading order', async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH});
  try {
    const page = await browser.newPage();
    await page.goto(url);
    await page.getByRole('button', {name:'Register',exact:true}).click();
    assert.match(await page.locator('#logo-preview').getAttribute('src'), /reverse/);
    assert.match(await page.locator('#current-logo-download').getAttribute('href'), /reverse/);
    await page.getByRole('button',{name:'Logos',exact:true}).click();
    assert.equal(await page.locator('.asset-item:visible').count(), 2);
    await page.getByRole('button',{name:'All',exact:true}).click();
    assert.ok(await page.locator('.asset-item:visible').count() > 5);
    await page.getByLabel('Test the voice').fill('From thought to direction.');
    assert.equal(await page.locator('#type-output').innerText(),'From thought to direction.');
    await page.setViewportSize({width:390,height:844});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth));
    assert.equal(await page.locator('h1').innerText(), 'Catalyst\nof analysis.');
  } finally { await browser.close(); }
});
