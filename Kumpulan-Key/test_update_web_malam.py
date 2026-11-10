"""Synthetic fixtures stay in an isolated temporary project, never in the release."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from update_web_malam import ROOT, update


class UpdateTests(unittest.TestCase):
    def test_release_and_reload(self):
        with tempfile.TemporaryDirectory(prefix='nusuk-updater-test-') as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'Salin-Kode-Nusuk', root / 'Salin-Kode-Nusuk')
            (root / 'Kumpulan-Key').mkdir()
            base = json.loads((root / 'Salin-Kode-Nusuk/BATCH-01.json').read_text())
            rows = [{'code': f'NG-T{i:07d}', 'source': 'https://example.com/synthetic-test'} for i in range(6000)]
            report = update(root, {'rows': rows[:2001] + rows[:1] + [{'code': base['codes'][0], 'source': 'https://example.com/old'}]})
            self.assertEqual(report['batchSizes'], [1000, 1000])
            self.assertEqual(report['pending'], 1)
            self.assertEqual(report['duplicatesSkippedThisRun'], 2)
            report = update(root, final=True)
            self.assertEqual(report['batchSizes'], [1000, 1000, 1])
            self.assertEqual(update(root, rows[:2001])['newUnique'], 2001)
            html = root / 'Salin-Kode-Nusuk/index.html'
            import hashlib
            self.assertEqual(report['html_sha256'], hashlib.sha256(html.read_bytes()).hexdigest())
            subprocess.run(['node', str(ROOT / 'Kumpulan-Key/test_release_merge.cjs'), str(html)], check=True)
            report = update(root, rows, final=True)
            self.assertEqual(report['newUnique'], 5000)
            self.assertEqual(report['totalWeb'], 6097)
            self.assertEqual(report['overLimitThisRun'], 1000)
            self.assertTrue(all(n <= 1000 for n in report['batchSizes']))
            before = html.read_bytes()
            with self.assertRaises(ValueError):
                update(root, [{'code': 'NG-invalid', 'source': ''}])
            self.assertEqual(before, html.read_bytes())
            from zipfile import ZipFile
            with ZipFile(root / 'Salin-Kode-Nusuk.zip') as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(z.read('Salin-Kode-Nusuk/index.html'), html.read_bytes())


if __name__ == '__main__':
    unittest.main()
