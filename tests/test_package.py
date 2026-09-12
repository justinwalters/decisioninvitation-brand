"""Release contract: catches incomplete, font-dependent or malformed deliveries."""
import json
import hashlib
import zipfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def test_release_manifest_matches_distributed_files(self):
        manifest = json.loads((ROOT/'releases/manifest.json').read_text())
        self.assertGreater(len(manifest['files']), 100)
        for entry in manifest['files']:
            data = (ROOT/entry['path']).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'], entry['path'])
            self.assertEqual(len(data), entry['bytes'])

    def test_download_kits_contain_real_assets_and_licenses(self):
        version = json.loads((ROOT/'brand-system.json').read_text())['version']
        for kind in ['brand', 'logos', 'templates', 'webfonts']:
            with zipfile.ZipFile(ROOT/f'releases/decisioninvitation-{kind}-{version}.zip') as bundle:
                self.assertIsNone(bundle.testzip())
                self.assertTrue(bundle.namelist())
                self.assertFalse(any(n.endswith('.zip') for n in bundle.namelist()))
                self.assertFalse(any('/.venv/' in n or '/.git/' in n or '/review/' in n for n in bundle.namelist()))
                if kind in ['brand','webfonts','templates']:
                    self.assertTrue(any('LICENSE-Sora' in n for n in bundle.namelist()))

    def test_all_lockups_are_font_independent_vectors(self):
        for kind in ['mark', 'wordmark', 'lockup', 'stacked', 'micro']:
            for variant in ['primary', 'reverse', 'ink', 'white']:
                p = ROOT / f'production/01-logo/svg/di-{kind}-{variant}.svg'
                self.assertTrue(p.exists(), f'Missing {p.name}')
                tree = ET.parse(p)
                tags = {e.tag.split('}')[-1] for e in tree.iter()}
                self.assertFalse(tags & {'text', 'image', 'script'}, p.name)
                self.assertIn('path', tags)

    def test_webfonts_and_licenses_are_distributed(self):
        for name in ['Sora-Regular.woff2', 'Sora-SemiBold.woff2', 'LICENSE-Sora.txt']:
            self.assertTrue((ROOT / 'assets/fonts' / name).is_file(), name)

    def test_static_font_names_distinguish_weights(self):
        from fontTools.ttLib import TTFont
        for style, weight in [('Regular', 400), ('SemiBold', 600)]:
            for extension in ['ttf', 'woff2']:
                font = TTFont(ROOT / f'assets/fonts/Sora-{style}.{extension}')
                self.assertIn('Sora', font['name'].getDebugName(6))
                self.assertEqual(font['name'].getDebugName(16) or font['name'].getDebugName(1), 'Sora')
                self.assertEqual(font['OS/2'].usWeightClass, weight)
                self.assertNotIn('fvar', font)

    def test_upstream_fonts_are_unmodified(self):
        provenance = json.loads((ROOT/'assets/fonts/provenance.json').read_text())
        self.assertEqual(len(provenance['files']), 4)
        for name, entry in provenance['files'].items():
            self.assertEqual(hashlib.sha256((ROOT/'assets/fonts'/name).read_bytes()).hexdigest(), entry['sha256'], name)
            self.assertTrue(entry['url'].startswith('https://raw.githubusercontent.com/'))

    def test_tokens_supply_accessible_semantic_roles(self):
        p = ROOT / 'assets/tokens/decisioninvitation.tokens.json'
        data = json.loads(p.read_text())
        self.assertIn('semantic', data)
        self.assertIn('focus', data.get('semantic', {}))
        self.assertNotEqual(data.get('semantic', {}).get('action'), '#D54B1E')

    def test_platform_exports_include_small_and_large_sizes(self):
        from PIL import Image
        for size in [16, 32, 48, 180, 192, 512, 1024]:
            p = ROOT / f'production/02-digital/di-icon-{size}.png'
            self.assertTrue(p.exists(), str(size))
            with Image.open(p) as im:
                self.assertEqual(im.size, (size, size))

if __name__ == '__main__':
    unittest.main()
