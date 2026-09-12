#!/usr/bin/env python3
"""Build deterministic, root-relative public identity kits from reviewed files.

This packages a proposal; it never approves, publishes, or deploys the identity.
The manifest inventories payload bytes. Archives embed that manifest; their own
checksums live alongside them to avoid a self-referential checksum cycle.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
KINDS = ('brand', 'logos', 'templates', 'webfonts')
ZIP_TIMESTAMP = (2026, 9, 12, 0, 0, 0)
TOP_FILES = {'README.md', 'BRAND-GUIDELINES.md', 'ASSET-LICENSE.md',
             'AGENTS.md', 'CHANGELOG.md', 'CONTRIBUTING.md', '.gitignore',
             'brand-system.json', 'package.json', 'package-lock.json', 'requirements.txt'}
PUBLIC_DIRS = ('assets', 'docs', 'output/pdf', 'production', 'site',
               'templates', 'tools', 'tests', '.github')
PRIVATE_PARTS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache',
                 'tmp', 'review', 'rendered', 'screenshots', 'archive', 'retired'}
FONT_LICENSES = ('assets/fonts/LICENSE-Sora.txt',)
MANUAL = 'output/pdf/decisioninvitation-identity-manual.pdf'
MANIFEST = 'releases/manifest.json'
COMMON = {'ASSET-LICENSE.md', 'brand-system.json', 'releases/README.md'}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def public_path(name):
    """Allow public source paths only; ZIP entries never follow symlinks."""
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name:
        return False
    if set(path.parts) & PRIVATE_PARTS:
        return False
    if name.startswith(('site/brand-assets/', 'production/05-proofs/web/')):
        return False
    if name == 'docs/adoption-register.md':
        return False
    if path.suffix.lower() in {'.zip', '.pyc', '.log'}:
        return False
    if path.name.startswith('.') and name != '.gitignore':
        return False
    if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'} and (
            'screenshot' in path.stem.lower() or path.stem.lower() == 'review'):
        return False
    if name.startswith('releases/') and name != 'releases/README.md':
        return False
    return True


def collect_files(root, kind='brand'):
    """Return sorted POSIX paths; keep repository hierarchy in every kit."""
    root = Path(root)
    if kind not in KINDS:
        raise ValueError(f'Unknown kit: {kind}')
    candidates = {name for name in TOP_FILES | {'releases/README.md'} if (root/name).is_file()}
    for folder in PUBLIC_DIRS:
        base = root / folder
        if not base.is_dir() or base.is_symlink():
            continue
        for directory, dirs, filenames in os.walk(base, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in PRIVATE_PARTS
                             and not (Path(directory)/d).is_symlink()
                             and public_path((Path(directory)/d/'placeholder').relative_to(root).as_posix()))
            for filename in filenames:
                path = Path(directory)/filename
                name = path.relative_to(root).as_posix()
                if not path.is_symlink() and public_path(name):
                    candidates.add(name)
    candidates = {name for name in candidates if public_path(name) and not (root/name).is_symlink()}
    if kind == 'brand':
        return sorted(candidates)
    if kind == 'logos':
        selected = lambda n: n.startswith('production/01-logo/') or n in {
            'docs/logo-standards.md', 'docs/color-and-accessibility.md'}
    elif kind == 'templates':
        selected = lambda n: n.startswith(('templates/', 'assets/fonts/', 'assets/tokens/',
                                           'production/01-logo/')) or n in {
            'docs/email-and-documents.md', 'docs/social-media-guidelines.md',
            'docs/messaging-and-voice.md', 'docs/claims-and-privacy.md',
            'docs/typography.md', 'docs/logo-standards.md'}
    else:
        selected = lambda n: n.startswith('assets/fonts/') or n in {'docs/typography.md'}
    return sorted(name for name in candidates if name in COMMON or selected(name))


def role_for(name):
    path = PurePosixPath(name)
    if name == MANUAL:
        return 'identity-manual'
    if name.startswith('assets/fonts/'):
        return 'font-license' if 'LICENSE' in path.name else 'font'
    if name.startswith('production/01-logo/'):
        return {'.svg': 'logo-vector', '.png': 'logo-raster', '.pdf': 'logo-pdf'}.get(path.suffix, 'logo-asset')
    if name.startswith('production/02-digital/'):
        return 'digital-icon'
    if name.startswith('production/03-social/'):
        return 'social-artwork'
    if name.startswith('production/05-proofs/'):
        return 'identity-overview'
    if name.startswith('assets/tokens/'):
        return 'design-tokens'
    if name.startswith(('assets/source/', 'assets/logo/')):
        return 'identity-source' if 'source/' in name else 'compatibility-logo'
    if name.startswith('templates/'):
        return 'editable-template'
    if name.startswith('site/'):
        return 'public-page-source'
    if name.startswith('tools/'):
        return 'build-tool'
    if name.startswith('tests/'):
        return 'quality-test'
    if name.startswith('.github/'):
        return 'continuous-integration'
    if path.name in {'requirements.txt', 'package.json', 'package-lock.json'}:
        return 'dependency-definition'
    if name == 'ASSET-LICENSE.md':
        return 'asset-usage-terms'
    return 'documentation'


def file_record(root, name):
    path = Path(root)/name
    data = path.read_bytes()
    record = {'path': name, 'role': role_for(name), 'bytes': len(data), 'sha256': sha256(data)}
    if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.ico'}:
        with Image.open(path) as im:
            record.update(width=im.width, height=im.height,
                          alpha=im.convert('RGBA').getchannel('A').getextrema()[0] < 255)
    elif path.suffix.lower() == '.svg':
        element = ET.fromstring(data)
        viewbox = element.get('viewBox', '').replace(',', ' ').split()
        if len(viewbox) == 4:
            width, height = map(float, viewbox[2:])
            record.update(width=int(width) if width.is_integer() else width,
                          height=int(height) if height.is_integer() else height)
    return record


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def write_zip(root, destination, names, manifest_bytes):
    """Stable ordering, permissions, timestamps and compression for fixed inputs."""
    root, destination = Path(root), Path(destination)
    if len(names) != len(set(names)) or MANIFEST in names:
        raise ValueError('Archive payload contains duplicate/reserved paths')
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted([*names, MANIFEST]):
            if name != MANIFEST and (not public_path(name) or (root/name).is_symlink()):
                raise ValueError(f'Unsafe archive path: {name}')
            info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, manifest_bytes if name == MANIFEST else (root/name).read_bytes(), compresslevel=9)


def build_release(root=ROOT):
    root = Path(root).resolve()
    for required in (MANUAL, 'docs/README.md'):
        if not (root/required).is_file() or not (root/required).stat().st_size:
            raise ValueError(f'Required manual/standards index missing: {required}')
    if not (root/MANUAL).read_bytes().startswith(b'%PDF-'):
        raise ValueError(f'Manual is not a PDF: {MANUAL}')
    for required in (*FONT_LICENSES, 'ASSET-LICENSE.md', 'package-lock.json'):
        if not (root/required).is_file():
            raise ValueError(f'Required release source or license missing: {required}')
    system = json.loads((root/'brand-system.json').read_text())
    version = system['version']
    if not all(part.isdigit() for part in version.split('.')) or len(version.split('.')) != 3:
        raise ValueError('Release version must be three numeric components')
    members = {kind: collect_files(root, kind) for kind in KINDS}
    for kind in ('brand', 'templates', 'webfonts'):
        if not set(FONT_LICENSES).issubset(members[kind]):
            raise ValueError(f'{kind} kit is missing the font license notices')
    for format_name in ('svg', 'png', 'pdf'):
        if not any(n.startswith(f'production/01-logo/{format_name}/') for n in members['logos']):
            raise ValueError(f'Logo kit has no {format_name.upper()} exports; rebuild before packaging')
    manifest = {
        'schemaVersion': '1.0', 'name': 'DecisionInvitation', 'version': version,
        'status': system.get('releaseStatus', 'proposal-pending-owner-review'),
        'archiveRoot': 'repository-relative; no enclosing directory',
        'checksumAlgorithm': 'SHA-256',
        'dimensions': 'PNG/ICO dimensions are pixels; SVG dimensions are viewBox units. Alpha means actual transparent pixels.',
        'exclusions': ['operational adoption ledger', 'private/review evidence', 'generated public mirror',
                       'caches and dependencies', 'nested ZIP archives'],
        'files': [file_record(root, name) for name in members['brand']],
        'kits': {kind: {'path': f'releases/decisioninvitation-{kind}-{version}.zip',
                        'files': members[kind]} for kind in KINDS},
    }
    destination = root/'releases'
    destination.mkdir(exist_ok=True)
    payload = json_bytes(manifest)
    (root/MANIFEST).write_bytes(payload)
    checksums = {'schemaVersion': '1.0', 'version': version, 'status': manifest['status'],
                 'algorithm': 'SHA-256', 'manifestSha256': sha256(payload), 'kits': []}
    for kind in KINDS:
        name = manifest['kits'][kind]['path']
        write_zip(root, root/name, members[kind], payload)
        data = (root/name).read_bytes()
        checksums['kits'].append({'path': name, 'bytes': len(data), 'sha256': sha256(data)})
    (destination/'checksums.json').write_bytes(json_bytes(checksums))
    return {'version': version, 'status': manifest['status'], 'payloadFiles': len(manifest['files']),
            'kits': checksums['kits']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='Identity repository root (default: this checkout)')
    args = parser.parse_args()
    try:
        print(json.dumps(build_release(args.root), indent=2))
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        parser.exit(1, f'Release refused: {error}\n')
