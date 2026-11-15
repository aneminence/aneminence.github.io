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
    content = source.read_text(encoding='utf-8-sig').encode('utf-8')
    digest = hashlib.sha256(content).hexdigest()[:12]
    versioned = f'{source.stem}.{digest}{source.suffix}'
    (OUT / versioned).write_bytes(content)
    # Transitional aliases for clients still holding pre-versioned HTML.
    # New HTML always uses the content-specific filename below.
    (OUT / name).write_bytes(content)
    html = html.replace(f'"{name}"', f'"{versioned}"')
def canonical_asset(path):
    if path.suffix.lower() in {'.svg', '.txt', '.json', '.css'}:
        return path.read_text(encoding='utf-8-sig').encode('utf-8')
    return path.read_bytes()

asset_paths = sorted((p for p in (ROOT / 'assets').rglob('*') if p.is_file()), key=lambda p: p.relative_to(ROOT).as_posix())
version_input = html.encode('utf-8') + b''.join(canonical_asset(p) for p in asset_paths)
version = hashlib.sha256(version_input).hexdigest()[:16]
html = html.replace('</head>', f'  <meta name="site-version" content="{version}" />\n</head>')
(OUT / 'index.html').write_text(html, encoding='utf-8')
for name in ('robots.txt', 'sitemap.xml', '.nojekyll'):
    shutil.copyfile(ROOT / name, OUT / name)
for source in asset_paths:
    target = OUT / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(canonical_asset(source))
print('Published files prepared in _site with content-versioned styles and scripts.')
