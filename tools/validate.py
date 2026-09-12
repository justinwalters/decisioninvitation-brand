#!/usr/bin/env python3
"""Verify identity consistency, export safety, local references and release integrity.

No network requests or publication. Passing this check is local technical evidence,
not visual approval, trademark clearance, print certification, or live acceptance.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PALETTE = {'ink': '#182B33', 'paper': '#F5F4EF', 'mist': '#E4ECEA',
           'field': '#52766D', 'orange': '#D54B1E', 'white': '#FFFFFF'}


def contrast(first, second):
    def luminance(value):
        values = [int(value[i:i+2], 16)/255 for i in (1, 3, 5)]
        linear = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in values]
        return sum(c*w for c, w in zip(linear, (.2126, .7152, .0722)))
    bright, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (bright+.05)/(dark+.05)


def read_json(root, name):
    return json.loads((Path(root)/name).read_text(encoding='utf-8'))


def check_identity(root):
    issues = []
    try:
        source = read_json(root, 'assets/source/identity.json')
        system = read_json(root, 'brand-system.json')
        tokens = read_json(root, 'assets/tokens/decisioninvitation.tokens.json')
        package = read_json(root, 'package.json')
        versions = [source.get('version'), system.get('version'), tokens.get('system', {}).get('version'), package.get('version')]
        if len(set(versions)) != 1 or not versions[0]:
            issues.append(f'Version drift across source/system/tokens/package: {versions}')
        if (Path(root)/'package-lock.json').exists():
            lock = read_json(root, 'package-lock.json')
            if lock.get('version') != versions[0] or lock.get('packages', {}).get('', {}).get('version') != versions[0]:
                issues.append('Lockfile version differs from identity version')
            if lock.get('packages', {}).get('', {}).get('devDependencies') != package.get('devDependencies'):
                issues.append('Lockfile dependency declarations differ from package.json')
        for label, colors in [('source', source.get('colors')), ('brand-system', system.get('identity', {}).get('palette')),
                              ('tokens', tokens.get('primitive', {}).get('color'))]:
            if colors != PALETTE:
                issues.append(f'{label} palette differs from the version 0.2.0 identity palette')
        semantic = tokens.get('semantic', {})
        expected = {'surface': PALETTE['paper'], 'text': PALETTE['ink'], 'textMuted': PALETTE['field'],
                    'action': PALETTE['ink'], 'onAction': PALETTE['paper'], 'focus': PALETTE['ink'],
                    'signature': PALETTE['orange']}
        for key, value in expected.items():
            if semantic.get(key) != value:
                issues.append(f'Semantic token {key} must be {value}, received {semantic.get(key)}')
        css = (Path(root)/'assets/tokens/decisioninvitation.tokens.css').read_text()
        for key, value in {**PALETTE, **{'action': PALETTE['ink'], 'on-action': PALETTE['paper'], 'focus': PALETTE['ink']}}.items():
            if not re.search(r'--di-' + re.escape(key) + r'\s*:\s*' + re.escape(value) + r'\s*;', css, re.I):
                issues.append(f'CSS token --di-{key} is missing or stale')
        for key in ('display', 'body', 'utility'):
            actual = [source.get('typography', {}).get(key), system.get('identity', {}).get('typography', {}).get(key), tokens.get('font', {}).get(key)]
            if len(set(actual)) != 1 or not actual[0]:
                issues.append(f'Typography drift in {key}: {actual}')
        if source.get('idea') != system.get('strategy', {}).get('primaryIdea') or source.get('promise') != system.get('strategy', {}).get('supportingPromise'):
            issues.append('Central idea or supporting promise differs across source and brand-system')
        if system.get('releaseStatus') != 'proposal-pending-owner-review':
            issues.append('Proposal status changed: explicit owner decision and validator update required')
        if system.get('strategy', {}).get('acquisitionClaim') is not False:
            issues.append('Acquisition history must not be asserted by this proposed identity')
        for label, first, second, minimum in [('Ink/Paper', 'ink', 'paper', 13.30), ('Field/Paper', 'field', 'paper', 4.5)]:
            if contrast(PALETTE[first], PALETTE[second]) < minimum:
                issues.append(f'{label} contrast is below its specified minimum')
        if contrast(semantic.get('onAction', '#000000'), semantic.get('action', '#000000')) < 4.5:
            issues.append('Primary action foreground/background contrast fails 4.5:1')
    except (OSError, ValueError, KeyError, TypeError) as error:
        issues.append(f'Cannot validate identity: {error}')
    return issues


def check_exports(root):
    root, issues = Path(root), []
    for path in sorted((root/'production').rglob('*.svg')):
        if 'web' in path.parts:
            continue
        name = path.relative_to(root).as_posix()
        try:
            tree = ET.parse(path)
            tags = {node.tag.split('}')[-1] for node in tree.iter()}
            unsafe = tags & {'text', 'image', 'script', 'foreignObject'}
            if unsafe:
                issues.append(f'{name}: SVG contains prohibited {", ".join(sorted(unsafe))}; use outlined vectors')
            if 'path' not in tags:
                issues.append(f'{name}: SVG has no outlined path artwork')
            for node in tree.iter():
                for key, value in node.attrib.items():
                    if key.split('}')[-1].lower().startswith('on'):
                        issues.append(f'{name}: SVG has an event handler')
                    if key.split('}')[-1] == 'href' and value and not value.startswith('#'):
                        issues.append(f'{name}: SVG has an external reference')
        except (OSError, ET.ParseError) as error:
            issues.append(f'{name}: invalid SVG ({error})')
    for path in sorted((root/'production/01-logo/png').glob('*.png')):
        try:
            with Image.open(path) as im:
                if im.convert('RGBA').getchannel('A').getextrema()[0] == 255:
                    issues.append(f'{path.relative_to(root)}: logo PNG must contain actual transparency')
                if im.width <= 0 or im.height <= 0:
                    issues.append(f'{path.relative_to(root)}: invalid raster dimensions')
        except OSError as error:
            issues.append(f'{path.relative_to(root)}: invalid PNG ({error})')
    for path in sorted((root/'production/01-logo/pdf').glob('*.pdf')):
        if not path.read_bytes().startswith(b'%PDF-'):
            issues.append(f'{path.relative_to(root)}: invalid PDF header')
    return issues


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(values['id'])
        for key in ('src', 'href', 'poster'):
            if values.get(key):
                self.links.append(values[key])
        if values.get('srcset'):
            self.links.extend(item.strip().split()[0] for item in values['srcset'].split(',') if item.strip())


def local_target(root, source, reference, public_mirror=False):
    parts = urlsplit(reference)
    if parts.scheme or parts.netloc or reference.startswith(('data:', 'mailto:', 'tel:')):
        return None
    path = unquote(parts.path)
    if not path:
        return source
    if path in {'/', '/brand', '/brand/'}:
        return None  # Product/server routes are separately verified after deployment.
    if path.startswith('/brand-assets/'):
        base = root/'site/brand-assets' if public_mirror else root
        return base/path.removeprefix('/brand-assets/')
    if path.startswith('/'):
        return root/'site'/path.lstrip('/')
    return source.parent/path


def check_links(root, public_mirror=False):
    root, issues = Path(root).resolve(), []
    site = root/'site'
    for source in sorted(site.rglob('*')):
        if not source.is_file() or source.suffix not in {'.html', '.css'} or 'brand-assets' in source.relative_to(site).parts:
            continue
        body = source.read_text(encoding='utf-8')
        parsed = References()
        if source.suffix == '.html':
            parsed.feed(body)
        references = list(parsed.links)
        references.extend(match[1].strip() for match in re.findall(r'url\(\s*([\'\"]?)(.*?)\1\s*\)', body))
        for reference in references:
            target = local_target(root, source, reference, public_mirror)
            if target is None:
                continue
            if not target.resolve().is_relative_to(root):
                issues.append(f'{source.relative_to(root)}: unsafe local reference {reference}')
            elif not target.is_file():
                issues.append(f'{source.relative_to(root)}: missing local target {reference}')
            elif urlsplit(reference).fragment and target.suffix == '.html':
                target_parser = parsed
                if target != source:
                    target_parser = References()
                    target_parser.feed(target.read_text(encoding='utf-8'))
                if unquote(urlsplit(reference).fragment) not in target_parser.ids:
                    issues.append(f'{source.relative_to(root)}: missing fragment {reference}')
    return issues


def package_module():
    spec = importlib.util.spec_from_file_location('di_package_release', Path(__file__).with_name('package_release.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_release(root):
    root, issues = Path(root), []
    package = package_module()
    try:
        manifest = read_json(root, package.MANIFEST)
        checksums = read_json(root, 'releases/checksums.json')
        version = read_json(root, 'brand-system.json')['version']
        if manifest.get('version') != version or checksums.get('version') != version:
            issues.append('Release metadata version differs from canonical identity')
        if manifest.get('status') != 'proposal-pending-owner-review' or checksums.get('status') != manifest.get('status'):
            issues.append('Release proposal status is absent or inconsistent')
        entries = manifest.get('files', [])
        names = [entry['path'] for entry in entries]
        if names != package.collect_files(root, 'brand'):
            issues.append('Release manifest does not exactly match current public payload; repackage after source changes')
        if len(names) != len(set(names)):
            issues.append('Release manifest contains duplicate paths')
        records = {entry['path']: entry for entry in entries}
        for entry in entries:
            name = entry['path']
            if not package.public_path(name) or (root/name).is_symlink():
                issues.append(f'Unsafe manifest path: {name}')
                continue
            if not (root/name).is_file():
                issues.append(f'Manifest file missing: {name}')
                continue
            if package.file_record(root, name) != entry:
                issues.append(f'Stale checksum, role or dimensions: {name}')
        manifest_bytes = (root/package.MANIFEST).read_bytes()
        if checksums.get('manifestSha256') != package.sha256(manifest_bytes):
            issues.append('Release manifest SHA-256 does not match checksums.json')
        checksum_entries = checksums.get('kits', [])
        archive_records = {item['path']: item for item in checksum_entries}
        expected_archives = {f'releases/decisioninvitation-{kind}-{version}.zip' for kind in package.KINDS}
        if set(archive_records) != expected_archives or len(checksum_entries) != len(expected_archives):
            issues.append('Archive checksums must list exactly the four versioned kits')
        if set(manifest.get('kits', {})) != set(package.KINDS):
            issues.append('Manifest must define exactly the four public kits')
        for kind in package.KINDS:
            name = f'releases/decisioninvitation-{kind}-{version}.zip'
            path = root/name
            if not path.is_file():
                issues.append(f'Missing kit: {name}')
                continue
            data = path.read_bytes()
            if archive_records.get(name) != {'path': name, 'bytes': len(data), 'sha256': package.sha256(data)}:
                issues.append(f'Archive checksum/size mismatch: {name}')
            members = package.collect_files(root, kind)
            if manifest.get('kits', {}).get(kind) != {'path': name, 'files': members}:
                issues.append(f'Manifest kit membership is stale: {kind}')
            with zipfile.ZipFile(path) as archive:
                if archive.testzip() is not None:
                    issues.append(f'Archive CRC failed: {name}')
                actual = archive.namelist()
                if actual != sorted([*members, package.MANIFEST]):
                    issues.append(f'Archive file list is wrong or duplicated: {name}')
                for info in archive.infolist():
                    item = info.filename
                    if item != package.MANIFEST and not package.public_path(item):
                        issues.append(f'Unsafe/nested archive entry: {name}: {item}')
                    if info.date_time != package.ZIP_TIMESTAMP:
                        issues.append(f'Non-deterministic archive timestamp: {name}: {item}')
                    content = archive.read(item)
                    if item == package.MANIFEST:
                        if content != manifest_bytes:
                            issues.append(f'Embedded manifest differs: {name}')
                    elif item not in records or package.sha256(content) != records[item]['sha256'] or len(content) != records[item]['bytes']:
                        issues.append(f'Archive payload differs from inventory: {name}: {item}')
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
        issues.append(f'Cannot verify release integrity: {error}')
    return issues


def validate(root=ROOT, require_release=True, public_mirror=False):
    issues = check_identity(root) + check_exports(root) + check_links(root, public_mirror)
    if require_release:
        issues.extend(check_release(root))
    return issues


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--source-only', action='store_true', help='Skip release checks while authoring (download links still require files)')
    parser.add_argument('--public-mirror', action='store_true', help='Check /brand-assets URLs against the generated site mirror, not canonical files')
    args = parser.parse_args()
    problems = validate(args.root, not args.source_only, args.public_mirror)
    for problem in problems:
        print(f'FAIL: {problem}')
    if problems:
        raise SystemExit(1)
    print('PASS: versions, palette, typography, semantic contrast, outlined SVGs, logo transparency, and local page references.')
    if not args.source_only:
        print('PASS: complete public inventory, SHA-256 checksums, deterministic archive metadata, exclusions, and all four ZIP payloads.')
    print(f'Contrast: Ink/Paper {contrast(PALETTE["ink"], PALETTE["paper"]):.2f}:1; Field/Paper {contrast(PALETTE["field"], PALETTE["paper"]):.2f}:1; Paper/Ink action {contrast(PALETTE["paper"], PALETTE["ink"]):.2f}:1.')
    print('Local technical verification only. Owner approval, visual/print review, publication and live acceptance are separate gates.')
