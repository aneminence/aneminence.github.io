"""Subset the licensed VI fonts for this website. Requires fonttools[woff].
Run from the repository: python scripts/prepare_fonts.py --brand ../aneminence-brand
"""
from pathlib import Path
import argparse,json,hashlib,shutil
from fontTools import subset
from fontTools.ttLib import TTFont
parser=argparse.ArgumentParser()
parser.add_argument('--brand',type=Path,default=Path(__file__).resolve().parents[2]/'aneminence-brand')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
source=args.brand/'assets/typography'
out=ROOT/'assets/fonts';out.mkdir(parents=True,exist_ok=True)
content=''.join((ROOT/name).read_text(encoding='utf-8-sig') for name in ('index.html','projects.js','main.js'))
latin=set(range(32,256))|set(range(0x2000,0x2070))|{0x2197,0x2198,0x2191,0x2193}
chinese={ord(c) for c in content if ord(c)>=0x2e80}|set(range(0x3000,0x3040))|set(range(0xff00,0xff60))
records=[]
for original,output,unicodes in [('Inter.ttf','inter-latin.woff2',latin),('NotoSansSC.ttf','noto-sans-sc-site.woff2',chinese)]:
 font=TTFont(source/'fonts'/original,recalcTimestamp=False)
 options=subset.Options();options.flavor='woff2'
 processor=subset.Subsetter(options=options);processor.populate(unicodes=unicodes);processor.subset(font)
 font.flavor='woff2';font.save(out/output)
 records.append({'original':original,'output':output,'bytes':(out/output).stat().st_size,'sourceSHA256':hashlib.sha256((source/'fonts'/original).read_bytes()).hexdigest()})
for name in ('Inter-OFL.txt','NotoSansSC-OFL.txt'):shutil.copyfile(source/'licenses'/name,out/name)
(out/'sources.json').write_text(json.dumps({'license':'SIL OFL 1.1; licenses retained alongside fonts','source':'aneminence VI 2.0 licensed font files; Google Fonts official source','subsets':records},indent=2),encoding='utf-8')
print(json.dumps(records,indent=2))
