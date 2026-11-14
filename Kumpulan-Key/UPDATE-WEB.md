# Overnight web updater

## Curated releases toward 7,777 (11 November 2026)

Owner: Takumi. Akira supplies curated rows with public source URLs and observation times.
Use `python Kumpulan-Key/release_curated.py --input C:\absolute\path\stage.json`
for each partial stage. It appends a new batch of at most 1,000 keys, with a larger
final batch allowed only when it closes the total at exactly 7,777. It skips global
duplicates and rejects totals above 7,777. Run one writer at a time and review
the result before committing. Batch JSON retains the source rows. `UPDATE-KURASI.json`
reports the latest stage. Run `python Kumpulan-Key/test_update_web_malam.py` before push.

The overnight campaign below is closed. Its ledger and reports are historical;
do not rerun that updater on the published project because it rebuilds its own
batch list. The curated release command preserves those historical files.

Owner: Takumi (web and ZIP). Search and scheduling remain with Akira.
Campaign: malam-20261110. Baseline: BATCH-01.json, 1,099 keys (1,097 original plus two supplied by Fathah on 11 November 2026).

Run from the existing project root:

```powershell
python Kumpulan-Key\update_web_malam.py --input "C:\absolute\path\collected.json"
```

Input is a JSON array or an object with `rows`. Each row must contain `code`
(exact NG- plus eight alphanumeric characters, case preserved) and `source`
(the URL where that code was actually observed). Optional context and collectedAt
are retained. Do not synthesize codes or mark application acceptance.

All rows are validated before writes. Global deduplication covers packaged batches
and every accepted row this night, including pending rows. The campaign accepts at
most 5,000 new keys. Output reports duplicates and keys beyond the cap.

Every complete group of 1,000 is released immediately. Pending keys remain in
`Kumpulan-Key/malam-20261110.json` until a group fills. Only at final closing:

```powershell
python Kumpulan-Key\update_web_malam.py --final
```

This releases the final partial group, if any. Subsequent runs are idempotent.
The same ledger repairs an interrupted publication on rerun. A process lock rejects
concurrent CLI writers. Do not edit the ledger or HTML concurrently.

Outputs are `Salin-Kode-Nusuk/index.html`, BATCH-02.json onward, kode-nusuk.txt,
UPDATE-MALAM.json, and the root Salin-Kode-Nusuk.zip. Batch JSON retains source rows.
HTML embeds the released batches for offline use. On reload, new releases appear
in the selector; existing copy history and personal batches are retained. Keys that
already exist in a personal batch are skipped in the packaged release on that device.
New releases become active once; later reloads preserve the selected batch.

Before replacing the web folder on a phone, use Backup. Replace files in the same
folder and refresh. Restore is available if browser storage changes with file origin.

Verification command:

```powershell
python Kumpulan-Key\test_update_web_malam.py
```

Verified locally on 10 November 2026: 2,001 -> 1,000 + 1,000 + 1,
repeat imports, old-key exclusion, 5,000 cap, rejected malformed input, ZIP equality,
legacy progress migration, reload, personal-batch overlaps, and copy history.
Fixtures only run in an isolated temporary directory. No new browser or physical
phone test was run for this updater revision. No Nusuk acceptance test was run.

Status at preparation: 0 new keys; 1,097 keys remain in the actual package.

## Winner recap through 13 November 2026

Owner: Takumi. Integrated on 14 November from the unchanged audit at
`../Rekap-Pemenang/Audit-Naoki-20261114`. The latest dataset is
`rekap-pemenang/kartu-01-13-nov2026.json`: 143 unique source cards,
130 Zamzam and 13 Umrah. The featured Umrah card duplicates list card 11
and is counted once. Names are omitted; country values remain app labels.

Data checks passed: audit JSON equals CSV, previous 132 records preserved,
IDs 133-143 appended, daily counts and 13 November country counts matched.
`python Kumpulan-Key/rekap-pemenang/render_chart.py` rebuilt PNG, PDF,
aggregate CSV and validation metadata. The chart was visually inspected.
The offline ZIP contains 22 files, each byte-identical to the web folder.
The local page was read in BrowserOS neo. Source screenshot and all audit
files retain their original SHA-256 hashes. No test suite was run, as requested;
the publication commit uses `[data-only]` to skip the CI test step.
Publication and live verification are reported with the resulting commit.
