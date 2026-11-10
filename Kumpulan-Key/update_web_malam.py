"""Release sourced Nusuk keys in groups of 1000. No network or dependencies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from datetime import datetime, timezone, timedelta
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = 'malam-20261110'


def dump(value):
    return json.dumps(value, ensure_ascii=True, indent=2) + '\n'


def atomic(path, data):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(data, encoding='utf-8')
    os.replace(tmp, path)


def update(root, incoming=None, final=False):
    root = Path(root)
    web = root / 'Salin-Kode-Nusuk'
    ledger_path = root / 'Kumpulan-Key' / 'malam-20261110.json'
    base = json.loads((web / 'BATCH-01.json').read_text(encoding='utf-8-sig'))
    ledger = json.loads(ledger_path.read_text(encoding='utf-8-sig')) if ledger_path.exists() else {
        'campaign': CAMPAIGN, 'limit': 5000, 'rows': [], 'batches': []}
    assert ledger['campaign'] == CAMPAIGN and ledger['limit'] == 5000
    known = set(base['codes'])
    for path in web.glob('BATCH-*.json'):
        known.update(json.loads(path.read_text(encoding='utf-8-sig'))['codes'])
    known.update(r['code'] for r in ledger['rows'])
    skipped = overflow = 0
    now = datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')
    if incoming is not None:
        rows = incoming.get('rows') if isinstance(incoming, dict) else incoming
        if not isinstance(rows, list):
            raise ValueError('Input must be an array or an object with rows.')
        for row in rows:
            if not isinstance(row, dict) or not re.fullmatch(r'NG-[A-Za-z0-9]{8}', row.get('code', '')):
                raise ValueError('Each row needs an exact NG- code with eight characters.')
            if not isinstance(row.get('source'), str) or not re.match(r'^https?://[^\s]+$', row['source']):
                raise ValueError('Each row needs a source URL.')
            if row['code'] in known:
                skipped += 1
                continue
            if len(ledger['rows']) >= 5000:
                overflow += 1
                continue
            ledger['rows'].append({**row, 'collectedAt': row.get('collectedAt', now)})
            known.add(row['code'])
    released = sum(len(b['codes']) for b in ledger['batches'])
    pending = ledger['rows'][released:]
    while len(pending) >= 1000 or (final and pending):
        chunk = pending[:1000]
        number = len(ledger['batches']) + 2
        ledger['batches'].append({
            'id': f'{CAMPAIGN}-{number:02d}', 'name': f'Batch {number:02d}',
            'createdAt': now, 'campaign': CAMPAIGN,
            'codes': [r['code'] for r in chunk], 'rows': chunk})
        pending = pending[len(chunk):]
    ledger['updatedAt'] = now
    ledger['pending'] = len(pending)
    ledger['newUnique'] = len(ledger['rows'])
    assert ledger['newUnique'] <= 5000
    assert all(0 < len(b['codes']) <= 1000 for b in ledger['batches'])
    html_path = web / 'index.html'
    html = html_path.read_text(encoding='utf-8-sig')
    expected = re.search(r'<script id="codeData" type="application/json">(.*?)</script>', html, re.S)
    assert json.loads(expected[1]) == base['codes'], 'Baseline mismatch'
    payload = [{k: b[k] for k in ('id', 'name', 'createdAt', 'codes')} for b in ledger['batches']]
    tag = '<script id="releasedBatches" type="application/json">' + json.dumps(payload) + '</script>'
    html, count = re.subn(r'<script id="releasedBatches" type="application/json">.*?</script>', lambda m: tag, html, flags=re.S)
    if not count:
        html = html.replace('<script>\n', tag + '\n<script>\n', 1)
    # Save the ledger first. Re-running repairs any interrupted release from this ledger.
    atomic(ledger_path, dump(ledger))
    for b in ledger['batches']:
        atomic(web / (b['name'].upper().replace(' ', '-') + '.json'), dump(b))
    atomic(html_path, html)
    all_codes = base['codes'] + [c for b in payload for c in b['codes']]
    assert len(all_codes) == len(set(all_codes))
    atomic(web / 'kode-nusuk.txt', '\n'.join(all_codes) + '\n')
    report = {'checkedAt': now, 'baseline': len(base['codes']), 'newUnique': ledger['newUnique'],
              'releasedNew': sum(len(b['codes']) for b in payload), 'pending': len(pending),
              'batchSizes': [len(b['codes']) for b in payload], 'totalWeb': len(all_codes),
              'duplicatesSkippedThisRun': skipped, 'overLimitThisRun': overflow,
              'html_sha256': hashlib.sha256(html_path.read_bytes()).hexdigest(),
              'nusuk_app_tested': False}
    atomic(web / 'UPDATE-MALAM.json', dump(report))
    zip_path = root / 'Salin-Kode-Nusuk.zip'
    with ZipFile(str(zip_path) + '.tmp', 'w', ZIP_DEFLATED) as z:
        for path in sorted(web.iterdir()):
            if path.is_file() and not path.name.endswith('.tmp'):
                z.write(path, 'Salin-Kode-Nusuk/' + path.name)
    os.replace(str(zip_path) + '.tmp', zip_path)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--final', action='store_true', help='Release the remaining partial batch at closing.')
    args = parser.parse_args()
    # Exclusive writer guard; the OS releases the file lock on process exit/crash.
    import msvcrt
    with open(ROOT / 'Kumpulan-Key' / 'update-web.lock', 'a+b') as lock:
        lock.seek(0)
        if not lock.read(1):
            lock.write(b'0')
            lock.flush()
        lock.seek(0)
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        data = json.loads(args.input.read_text(encoding='utf-8-sig')) if args.input else None
        print(dump(update(ROOT, data, args.final)))
