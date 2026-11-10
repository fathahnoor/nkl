# Overnight web updater

Owner: Takumi (web and ZIP). Search and scheduling remain with Akira.
Campaign: malam-20261110. Baseline: BATCH-01.json, 1,097 keys.

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
