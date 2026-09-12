const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
(async()=>{
  const browser = await chromium.launch({executablePath:process.env.CHROMIUM_PATH});
  const page = await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const out=path.resolve(__dirname,'../production/05-proofs/web');fs.mkdirSync(out,{recursive:true});
  await page.goto(process.env.BRAND_URL || 'http://127.0.0.1:3000/brand');await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:path.join(out,'brand-desktop.png'),fullPage:true});
  await page.screenshot({path:path.join(out,'brand-first-fold.png')});
  for(const id of ['system','identity','color','type','voice','resources'])await page.locator(`#${id}`).screenshot({path:path.join(out,`brand-${id}.png`)});
  const broken=await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src));
  const links=await page.locator('a[href^="/brand-assets/"]').evaluateAll(a=>[...new Set(a.map(i=>i.href))]);
  const downloads=[];for(const url of links){const r=await page.request.get(url);downloads.push({url,status:r.status(),type:r.headers()['content-type']});}
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>window.scrollTo({top:0,left:0,behavior:'instant'}));
  await page.waitForFunction(()=>window.scrollY===0);
  await page.screenshot({path:path.join(out,'brand-mobile-first-fold.png')});
  await page.screenshot({path:path.join(out,'brand-mobile.png'),fullPage:true});
  const overflow=await page.evaluate(()=>({width:innerWidth,document:document.documentElement.scrollWidth}));
  await page.setViewportSize({width:640,height:850});
  const zoomReflow=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
  console.log(JSON.stringify({errors,broken,overflow,zoomReflow,downloads},null,2));
  await browser.close();
  if(errors.length||broken.length||overflow.document>overflow.width||!zoomReflow||downloads.some(x=>x.status!==200))process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
