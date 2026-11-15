"""Package the static site with content-versioned CSS/JS (standard library only)."""
import hashlib
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
if OUT.exists():
    if OUT.is_symlink() or OUT.resolve() != ROOT / '_site':
        raise RuntimeError('Refusing to clean an output directory outside this repository.')
    shutil.rmtree(OUT)
OUT.mkdir(exist_ok=True)
html = (ROOT / 'index.html').read_text(encoding='utf-8-sig')
for name in ('styles.css', 'projects.js', 'main.js'):
    source = ROOT / name
    content = source.read_bytes()
    digest = hashlib.sha256(content).hexdigest()[:12]
    versioned = f'{source.stem}.{digest}{source.suffix}'
    (OUT / versioned).write_bytes(content)
    # Transitional aliases for clients still holding pre-versioned HTML.
    # New HTML always uses the content-specific filename below.
    (OUT / name).write_bytes(content)
    html = html.replace(f'"{name}"', f'"{versioned}"')
(OUT / 'index.html').write_text(html, encoding='utf-8')
for name in ('robots.txt', 'sitemap.xml', '.nojekyll'):
    shutil.copyfile(ROOT / name, OUT / name)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
print('Published files prepared in _site with content-versioned styles and scripts.')
