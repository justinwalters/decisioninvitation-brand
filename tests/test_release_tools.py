"""Public release boundaries and failure checks; no fixtures mutate the real repo."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_tool(name):
    path = ROOT / 'tools' / f'{name}.py'
    if not path.is_file():
        raise AssertionError(f'Required release tool is missing: {path.name}')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseBoundaryTests(unittest.TestCase):
    def test_public_payload_excludes_private_and_recursive_material(self):
        package = load_tool('package_release')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            allowed = ['README.md', 'tools/build.py', 'assets/fonts/font.woff2',
                       'docs/logo-standards.md', 'site/index.html',
                       'production/01-logo/svg/mark.svg', 'output/pdf/manual.pdf']
            excluded = ['.git/config', '.venv/lib/module.py', 'node_modules/a.js',
                        'tmp/log.txt', 'docs/adoption-register.md',
                        'templates/applications/review/card.png',
                        'production/05-proofs/web/desktop.png',
                        'output/rendered/page.png', 'site/brand-assets/file.svg',
                        'assets/old.ZIP', 'releases/manifest.json',
                        'site/review.png', 'tools/__pycache__/module.pyc']
            for name in allowed + excluded:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            actual = package.collect_files(root, 'brand')
            self.assertEqual(actual, sorted(allowed))

    def test_packaging_refuses_missing_manual_and_docs_index(self):
        package = load_tool('package_release')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'brand-system.json').write_text(json.dumps({'version': '0.2.0'}))
            with self.assertRaisesRegex(ValueError, 'manual|README'):
                package.build_release(root)
            self.assertFalse((root / 'releases').exists())

    def test_zip_writer_is_deterministic_and_root_relative(self):
        package = load_tool('package_release')
        import zipfile
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'assets/logo.svg'
            source.parent.mkdir()
            source.write_text('<svg/>')
            first, second = root / 'a.zip', root / 'b.zip'
            package.write_zip(root, first, ['assets/logo.svg'], b'{"version":"0.2.0"}\n')
            package.write_zip(root, second, ['assets/logo.svg'], b'{"version":"0.2.0"}\n')
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(archive.namelist(), ['assets/logo.svg', 'releases/manifest.json'])
                self.assertEqual(archive.read('assets/logo.svg'), b'<svg/>')
                self.assertTrue(all(item.date_time == package.ZIP_TIMESTAMP for item in archive.infolist()))


class ValidatorTests(unittest.TestCase):
    def test_color_contrast_uses_relative_luminance(self):
        validate = load_tool('validate')
        self.assertAlmostEqual(validate.contrast('#211B2B', '#F7F8FF'), 15.78, places=2)
        self.assertAlmostEqual(validate.contrast('#3346C8', '#F7F8FF'), 6.95, places=2)

    def test_identity_validation_rejects_palette_drift(self):
        validate = load_tool('validate')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ['assets/source/identity.json', 'brand-system.json',
                         'assets/tokens/decisioninvitation.tokens.json',
                         'assets/tokens/decisioninvitation.tokens.css', 'package.json']:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            self.assertEqual(validate.check_identity(root), [])
            path = root / 'assets/tokens/decisioninvitation.tokens.json'
            data = json.loads(path.read_text())
            data['primitive']['color']['register'] = '#000000'
            path.write_text(json.dumps(data))
            self.assertTrue(any('palette' in issue.lower() for issue in validate.check_identity(root)))

    def test_export_validation_rejects_text_and_opaque_logo(self):
        validate = load_tool('validate')
        from PIL import Image
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            svg = root / 'production/01-logo/svg/unsafe.svg'
            svg.parent.mkdir(parents=True)
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>Live type</text></svg>')
            png = root / 'production/01-logo/png/opaque.png'
            png.parent.mkdir()
            Image.new('RGBA', (20, 20), (0, 0, 0, 255)).save(png)
            issues = validate.check_exports(root)
            self.assertTrue(any('text' in issue for issue in issues))
            self.assertTrue(any('transparen' in issue for issue in issues))

    def test_link_validation_detects_missing_asset_and_fragment(self):
        validate = load_tool('validate')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'site').mkdir()
            (root / 'site/index.html').write_text('<main id="main"><a href="#main">ok</a><a href="#missing">bad</a><img src="/brand-assets/assets/no.svg"></main>')
            issues = validate.check_links(root)
            self.assertTrue(any('#missing' in issue for issue in issues))
            self.assertTrue(any('assets/no.svg' in issue for issue in issues))


if __name__ == '__main__':
    unittest.main()
