"""Browser regression checks. Requires Playwright. No production dependency.
python scripts/browser_check.py --url http://127.0.0.1:8872 --report ../website-reports
"""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8872');parser.add_argument('--report',type=Path,default=Path('../website-reports'));args=parser.parse_args();args.report.mkdir(parents=True,exist_ok=True)
results=[]
def check(browser,engine,width,height):
 context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce')
 page=context.new_page();errors=[];bad=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append({'status':r.status,'url':r.url}) if r.status>=400 and r.url.startswith(args.url) else None)
 response=page.goto(args.url,wait_until='networkidle');assert response.status==200
 page.evaluate('document.fonts.ready')
 assert page.locator('.project').count()==6
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert page.evaluate("getComputedStyle(document.documentElement).colorScheme")=='light only'
 assert page.evaluate("document.fonts.check('16px Inter') && document.fonts.check('16px \"Noto Sans SC\"')")
 overflow=page.evaluate("""()=>Array.from(document.querySelectorAll('.hero h1,.project-info h3,.manifesto h2,.contact h2,.works-heading h2')).filter(e=>{const r=e.getBoundingClientRect();return r.width&& (r.left<-.5||r.right>innerWidth+.5)}).map(e=>e.textContent)""")
 assert not overflow,overflow
 if width<=760:
  page.locator('#nav-toggle').click();assert page.locator('#nav-toggle').get_attribute('aria-expanded')=='true'
  page.locator('.main-nav a[href="#works"]').click();assert page.locator('#nav-toggle').get_attribute('aria-expanded')=='false'
  page.locator('#nav-toggle').click();page.keyboard.press('Escape');assert page.locator('#nav-toggle').get_attribute('aria-expanded')=='false'
 for category,count in [('studio',2),('labs',1),('craft',3),('all',6)]:
  chip=page.locator('.filter-chip[data-filter="'+category+'"]');chip.click();assert chip.get_attribute('aria-pressed')=='true';assert page.locator('.project:visible').count()==count
 for ident in ['identity','stationery','cmts','hardware','storage','apparel']:
  card=page.locator('[data-project="'+ident+'"]');card.click();assert page.locator('#project-modal').is_visible()
  page.locator('#modal-image').evaluate('(i)=>i.decode()')
  assert page.evaluate('document.activeElement.id')=='modal-close'
  assert page.locator('main').get_attribute('inert') is not None
  page.keyboard.press('Shift+Tab');assert page.evaluate('document.activeElement.id')=='modal-return'
  page.keyboard.press('Tab');assert page.evaluate('document.activeElement.id')=='modal-close'
  if ident=='cmts':
   assert '已上线' in page.locator('#modal-status').inner_text()
   assert page.locator('#modal-link').get_attribute('href')=='https://aneminence.github.io/cmts-website/zh/'
   assert '访问 CMTS 网站' in page.locator('#modal-link').inner_text()
  if ident=='hardware':assert page.locator('#modal-link').is_hidden()
  page.keyboard.press('Escape');assert page.locator('#project-modal').is_hidden()
  assert page.evaluate('document.activeElement.dataset.project')==ident
 for category in ['studio','labs','craft']:
  page.locator('[data-division="'+category+'"]').click();assert page.locator('.filter-chip.active').get_attribute('data-filter')==category
 page.locator('[data-filter="all"]').click()
 # Nonexistent category represents an empty content set; reset returns safely.
 page.evaluate("applyFilter('unavailable')");assert page.locator('#empty-state').is_visible();page.locator('#reset-filter').click();assert page.locator('.project:visible').count()==6
 page.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
 page.evaluate('Promise.all(Array.from(document.images).map(i=>i.decode()))')
 anchors=page.evaluate("""()=>Array.from(document.querySelectorAll('a[href^="#"]')).filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash)""")
 assert not anchors,anchors
 page.evaluate('scrollTo(0,0);document.activeElement.blur()');page.wait_for_function('scrollY===0')
 page.screenshot(path=str(args.report/f'{engine}-{width}.png'))
 if width==1440:
  page.locator('#works').screenshot(path=str(args.report/f'{engine}-works.png'),style='.site-header,.skip-link{visibility:hidden!important}')
 assert not errors,errors
 assert not bad,bad
 results.append({'engine':engine,'viewport':f'{width}x{height}','status':'pass','projectCount':6,'scriptErrors':errors,'failedResponses':bad,'overflow':overflow})
 context.close()
with sync_playwright() as pw:
 for engine,options,sizes in [('chromium',{'channel':'msedge','args':['--no-proxy-server']},[(320,812),(390,844),(768,1024),(1440,1000)]),('firefox',{},[(390,844),(1440,1000)]),('webkit',{},[(390,844),(1440,1000)])]:
  browser=getattr(pw,engine).launch(headless=True,**options)
  for width,height in sizes:check(browser,engine,width,height)
  browser.close()
 # Simulate missing thumbnails and detail imagery; the text and close controls remain usable.
 browser=pw.chromium.launch(channel='msedge',headless=True,args=['--no-proxy-server'])
 context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
 page=context.new_page();page.route('**/assets/projects/identity.svg',lambda route:route.abort())
 page.goto(args.url,wait_until='networkidle');card=page.locator('[data-project="identity"]');card.scroll_into_view_if_needed();card.locator('.image-fallback').wait_for(state='visible');card.click();page.locator('#modal-image-fallback').wait_for(state='visible');assert page.locator('#modal-description').inner_text();page.keyboard.press('Escape');context.close()
 # Verify authored light background with the same Edge auto-dark feature used by the user.
 browser.close()
 browser=pw.chromium.launch(channel='msedge',headless=True,args=['--no-proxy-server','--enable-features=WebContentsForceDark'])
 context=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='dark',reduced_motion='reduce')
 page=context.new_page();page.goto(args.url,wait_until='networkidle');page.locator('#about').scroll_into_view_if_needed()
 assert page.locator('#about').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(247, 247, 245)'
 page.locator('#about').screenshot(path=str(args.report/'edge-auto-dark-about.png'),style='.site-header,.skip-link{visibility:hidden!important}')
 context.close();browser.close()
(args.report/'browser-results.json').write_text(json.dumps({'runs':results,'emptyState':'pass','missingImageFallback':'pass','autoDarkAuthoredLight':'pass'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
