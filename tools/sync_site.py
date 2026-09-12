#!/usr/bin/env python3
"""Publish only allowlisted brand resources into the website's public asset tree."""
from pathlib import Path
import argparse, shutil

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ['assets/fonts', 'assets/tokens', 'production', 'docs', 'output/pdf', 'releases']
EXTENSIONS = {'.svg','.png','.ico','.woff2','.ttf','.json','.css','.md','.txt','.pdf','.zip'}

def sync(target):
    target.mkdir(parents=True, exist_ok=True)
    for folder in PUBLIC:
        source = ROOT / folder
        if not source.exists(): continue
        for file in sorted(source.rglob('*')):
            if not file.is_file() or file.is_symlink() or file.suffix.lower() not in EXTENSIONS: continue
            if 'review' in file.parts or 'rendered' in file.parts or 'web' in file.parts: continue
            if file.name == 'adoption-register.md': continue
            dest = target / file.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(file, dest)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', type=Path, help='Existing DecisionInvitation product checkout')
    args = parser.parse_args()
    sync(ROOT/'site/brand-assets')
    if args.product:
        if not (args.product/'PRODUCT.md').is_file(): raise SystemExit('Product checkout marker missing; refusing broad copy.')
        for src,dst in [('index.html','brand.html'),('brand.css','brand.css'),('brand.js','brand.js')]:
            shutil.copyfile(ROOT/'site'/src, args.product/dst)
        sync(args.product/'brand-assets')
    print('Synced public identity resources; unrelated product files were not changed.')
