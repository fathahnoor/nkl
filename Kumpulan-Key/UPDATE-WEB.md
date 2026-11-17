# Overnight web updater

## Winner recap through 17 November 2026

Owner: Takumi. Integrated on 18 November from unchanged evidence at
`../Rekap-Pemenang/Audit-Naoki-20261118`. Dataset:
`rekap-pemenang/kartu-01-17-nov2026.json`, 187 unique source cards,
170 Zamzam and 17 Umrah. Previous 176 records preserved; IDs 177-187
match audit JSON and CSV and the screenshot. Featured Umrah counted once;
names omitted. Country values are app labels, not proof of nationality or
prize receipt. Audit and screenshot hashes unchanged.

Data/render checks: 17 days, each with 10 Zamzam and one Umrah.
17 November Zamzam: Pakistan 4, Sudan 1, Indonesia 1, India 1, Morocco 1,
Bangladesh 1, Egypt 1; Umrah: Egypt 1. Aggregate: 408 cells, sum 187.
PNG: 2368 x 3024; PDF rebuilt. ZIP: 26 files, byte-identical to web folder.
No test suite run; existing [data-only] CI path skips the test step.
Publication and BrowserOS neo verification reported with the release commit.

## Winner recap through 16 November 2026

Owner: Takumi. Integrated on 17 November from unchanged evidence at
`../Rekap-Pemenang/Audit-Naoki-20261117`. Dataset:
`rekap-pemenang/kartu-01-16-nov2026.json`, 176 unique source cards,
160 Zamzam and 16 Umrah. Previous 165 records preserved; IDs 166-176
match audit JSON and CSV. Featured Umrah counted once; names omitted.
Country values are app labels and do not prove nationality or prize receipt.

Data/render checks passed: 16 days, each with 10 Zamzam and one Umrah.
16 November: Pakistan 3, Sudan 1, Egypt 2, India 1, Saudi Arabia 1,
Bangladesh 2 for Zamzam; Senegal 1 for Umrah. Aggregate: 384 cells,
sum 176. PNG (2264 x 3024) visually checked; PDF rebuilt. ZIP: 25 files,
all byte-identical to the web folder. Audit and screenshot hashes unchanged.
No test suite run; existing [data-only] CI path skips the test step.
Publication and BrowserOS neo live verification reported with final commit.

## Winner recap through 15 November 2026

Owner: Takumi. Integrated on 16 November from the unchanged audit at
`../Rekap-Pemenang/Audit-Naoki-20261116`. Current dataset:
`rekap-pemenang/kartu-01-15-nov2026.json`, 165 unique source cards,
150 Zamzam and 15 Umrah. The previous 154 records are preserved.
IDs 155-165 match the audit JSON and CSV. The featured Umrah duplicate
is counted once. Names are omitted; country values remain app labels.

Data and render checks passed: 15 days with 10 Zamzam and one Umrah card
each; 15 November Zamzam totals match India 1, Saudi Arabia 2, Egypt 3,
Syria 1, Bangladesh 2 and Pakistan 1, plus one Indonesia Umrah card.
The chart has 345 cells summing to 165; PNG and PDF were rebuilt and the
PNG visually inspected. The offline ZIP contains 24 files, all byte-identical
to the web folder. All source audit files retain their SHA-256 hashes.
No test suite was run; `[data-only]` skips the existing CI test step.

BrowserOS neo is connected again. The previously pending 14 November
public recap was read on 16 November and showed 154 cards, 140 Zamzam
and 14 Umrah. Deployment and the 15 November live recap are checked
after push and reported with the publication commit.

## Winner recap through 14 November 2026

Owner: Takumi. Integrated on 15 November from the unchanged audit at
`../Rekap-Pemenang/Audit-Naoki-20261115`. Current dataset:
`rekap-pemenang/kartu-01-14-nov2026.json`, 154 unique cards,
140 Zamzam and 14 Umrah. Previous 143 records are preserved.
IDs 144-154 match the audit JSON and CSV; the featured Umrah card is
counted once. Names are omitted. Country values remain app labels,
and the screenshot does not prove receipt of a prize.

Render assertions passed for daily totals and country counts, including
Egypt 3, Pakistan 3, India 2, Senegal 1 and Saudi Arabia 1 for Zamzam
on 14 November, plus one Pakistan Umrah card. PNG and PDF were rebuilt,
and the PNG was visually inspected locally. The aggregate contains 294
cells summing to 154. The new Senegal flag binary comes from flagcdn.com;
its URL and SHA-256 are recorded in `rekap-pemenang/sumber.json`.
The offline ZIP contains 23 files, each byte-identical to the web folder.
All four audit files, including the screenshot, retain their SHA-256 hashes.
No test suite was run; `[data-only]` skips the existing CI test step.

Browser verification is pending: the configured BrowserOS neo MCP endpoint
at localhost:9010 did not answer the connection test on 15 November.
Restore BrowserOS neo, then check the live recap and chart at
https://fathahnoor.github.io/nkl/#rekap-pemenang.
Deployment status is reported with the publication commit.

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
