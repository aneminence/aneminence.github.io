"""Validate local release assets or an actual HTTPS Pages deployment (stdlib)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
from urllib.request import Request,urlopen
import argparse,re,time
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.urls=[];self.ids=set();self.anchors=[];self.version=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='meta' and a.get('name')=='site-version':self.version=a.get('content')
  for key in ['src','href']:
   u=a.get(key,'')
   if u.startswith('#'):self.anchors.append(u[1:])
   elif u and not urlsplit(u).scheme and not u.startswith('//'):self.urls.append(u)
parser=argparse.ArgumentParser();parser.add_argument('--url');args=parser.parse_args()
html=(ROOT/'_site/index.html').read_text(encoding='utf-8');local=Page();local.feed(html)
assert local.version,'Missing build version'
assert all(a in local.ids for a in local.anchors),'Broken internal anchor'
paths=set(local.urls)
for source in ['styles.css','projects.js']:
 paths.update(re.findall(r"assets/[a-zA-Z0-9_./-]+",(ROOT/source).read_text(encoding='utf-8')))
for name in paths:assert (ROOT/'_site'/unquote(urlsplit(name).path)).is_file(),f'Missing local asset: {name}'
if args.url:
 assert args.url.startswith('https://'),'Published site must use HTTPS'
 error=None
 for attempt in range(12):
  try:
   request=Request(args.url+'?verify='+local.version,headers={'User-Agent':'aneminence-deploy-check','Cache-Control':'no-cache'})
   with urlopen(request,timeout=20) as response:
    assert response.status==200 and response.url.startswith('https://')
    live=Page();live.feed(response.read().decode('utf-8'))
   assert live.version==local.version,'CDN is still serving an earlier build'
   for name in paths:
    with urlopen(Request(urljoin(args.url,name),headers={'User-Agent':'aneminence-deploy-check'}),timeout=20) as response:
     assert response.status==200 and len(response.read(128))>0,f'Empty published asset: {name}'
   error=None;break
  except Exception as exc:
   error=exc
   if attempt<11:time.sleep(10)
 if error:raise SystemExit(f'Public verification failed: {error}')
 print(f'HTTPS release verified: {local.version}, {len(paths)} assets')
else:print(f'Local release verified: {local.version}, {len(paths)} assets and {len(local.anchors)} anchors')
