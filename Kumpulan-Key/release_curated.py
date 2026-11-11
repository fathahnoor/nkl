"""Append a curated partial batch, preserving all previous releases and ledgers."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def release(root, incoming):
    root = Path(root)
    web = root / 'Salin-Kode-Nusuk'
    paths = sorted(web.glob('BATCH-*.json'))
    batches = [json.loads(p.read_text(encoding='utf-8-sig')) for p in paths]
    codes = [c for b in batches for c in b['codes']]
    assert len(codes) == len(set(codes)), 'Existing batches contain duplicates'
    rows = incoming.get('rows') if isinstance(incoming, dict) else incoming
    if not isinstance(rows, list):
        raise ValueError('Expected rows array')
    known, accepted = set(codes), []
    for row in rows:
        if not isinstance(row, dict) or not re.fullmatch(r'NG-[A-Za-z0-9]{8}', row.get('code', '')):
            raise ValueError('Invalid code')
        if not re.fullmatch(r'https?://[^\s]+', row.get('source', '')) or not row.get('collectedAt'):
            raise ValueError('Source URL and observation time required')
        datetime.fromisoformat(row['collectedAt'].replace('Z', '+00:00'))
        if row['code'] not in known:
            accepted.append(row)
            known.add(row['code'])
    if not accepted:
        return {'added': 0, 'totalWeb': len(codes)}
    if len(known) > 7777 or (len(accepted) > 1000 and len(known) != 7777):
        raise ValueError('Batch exceeds 1000 keys without closing at 7777, or total exceeds 7777')
    html_path = web / 'index.html'
    html = html_path.read_bytes().decode('utf-8-sig')
    match = re.search(r'<script id="releasedBatches" type="application/json">(.*?)</script>', html, re.S)
    payload = json.loads(match[1])
    assert [b['codes'] for b in payload] == [b['codes'] for b in batches[1:]], 'Embedded batch mismatch'
    number = max(int(p.stem.split('-')[1]) for p in paths) + 1
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    batch = {'id': f'kurasi-7777-{number:02d}', 'name': f'Batch {number:02d}',
             'createdAt': now, 'campaign': 'kurasi-7777',
             'codes': [r['code'] for r in accepted], 'rows': accepted}
    if isinstance(incoming, dict):
        batch.update({k: incoming[k] for k in ('attribution', 'reusePolicy') if k in incoming})
    payload.append({k: batch[k] for k in ('id', 'name', 'createdAt', 'codes')})
    html = html[:match.start(1)] + json.dumps(payload) + html[match.end(1):]
    report = {'checkedAt': now, 'added': len(accepted), 'totalWeb': len(known),
              'batch': batch['name'], 'duplicatesSkipped': len(rows)-len(accepted),
              'html_sha256': hashlib.sha256(html.encode()).hexdigest(), 'nusuk_app_tested': False}
    def write(path, value):
        path.write_bytes((json.dumps(value, ensure_ascii=True, indent=2)+'\n').encode())
    write(web / f'BATCH-{number:02d}.json', batch)
    html_path.write_bytes(html.encode())
    txt = web / 'kode-nusuk.txt'
    newline = '\r\n' if b'\r\n' in txt.read_bytes() else '\n'
    txt.write_bytes((newline.join(codes+batch['codes'])+newline).encode())
    write(web / 'UPDATE-KURASI.json', report)
    with ZipFile(root / 'Salin-Kode-Nusuk.zip', 'w', ZIP_DEFLATED) as z:
        for p in sorted(web.iterdir()):
            if p.is_file():
                z.write(p, 'Salin-Kode-Nusuk/'+p.name)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(release(ROOT, json.loads(args.input.read_text(encoding='utf-8-sig'))), indent=2))
