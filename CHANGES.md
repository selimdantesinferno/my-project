# all_in_one.py — Branch `claude/focused-ptolemy-BHhcd`

PyQt6 blog automation tool. Session changes layered on top of the
pre-existing 14,196-line script.

| metric | before | after |
|---|---|---|
| line count | 14,196 | 17,117 |
| top-level Agency classes | 0 | 6 |
| sidebar items in 글수집 | 12 | 1 |
| persisted state files | 0 | 5 JSON + N XLSX |

Final file is `all_in_one.py`. Each commit also shipped a sibling
`all_in_one_*.txt` snapshot for download (PyCharm couldn't accept
`.py` uploads cleanly).

---

## 1. Sidebar consolidation

### `UnifiedCollectPage` (commit `3e80934`)
The 글수집 group used to expand to 12 sub-entries (블로그 / 숏텐츠 /
다음 / 네이트 / 카페 / 인기글 / 유튜브 / 엑셀 + 4 살구 sub-pages).
Replaced with a single sidebar item that opens one page hosting all
of them via a top button bar + `QStackedWidget`. Existing page
classes are untouched and lazy-loaded.

Key change in `PostPro`: new `get_or_create_page(key)` helper so the
sidebar entry and the unified page can share the same page instance.

### `AgencyCategoryPage` (commit `a41b5f9`)
Same pattern for the new 대행/후기성 group: one sidebar item, five
large pill-style top tabs (`52px` min height, gold when selected) for
단계별진행 / 키워드 / 형태소 / 이미지 / 업로드.

---

## 2. New 대행/후기성 module

Added a 4-page Korean blog-agency workflow (commit `7c8ff23`):

| page | class | role |
|---|---|---|
| 키워드 지수확인 | `AgencyKeywordPage`     | ma-pia.net 연관키워드 → lablog.co.kr 키워드 대량조회 |
| 형태소 분석   | `AgencyMorphologyPage`  | Naver blog top-N analysis → GPT SEO titles           |
| 이미지       | `AgencyImagePage`       | gpt-image-1 edit (upload) + body→prompt generation   |
| 업로드       | `AgencyUploadPage`      | Naver blog publish, reuses existing helpers          |

Followed by a wizard (commit `3d2b66c`):

### `AgencyWizardPage` — 10-step
`소스선택 → 추출 → 블로그 → AI → 프롬프트 → 포스팅설정 → 이미지 → 스타일 → 백링크 → 포스팅`

- Top chip-stepper. Chips are `QPushButton`s so the user can jump
  back to any step (backward = free; forward re-runs intermediate
  `_on_exit_*` validators).
- Left half: per-step `QStackedWidget` + always-visible items table
  (#/글감/이미지/상태/확대/링크).
- Right half: in-page log panel mirrored to `main.log`.
- Items table `↗` opens a preview dialog with 원본 / AI 재작성 /
  이미지 경로 tabs.
- ⑩ 포스팅 starts a worker that does extract → AI rewrite → image
  → backlinks → upload per item. Upload is a simulation right now;
  the wiring is in place to call `AgencyUploadPage._do_upload`.

Stepper was bumped from `11px` to `14–15px` with 40–52px height
(commit `a41b5f9`).

---

## 3. Auto-persistence (commit `6bb32c8`)

Crashes were losing partially-completed work, so every Agency page
now writes state to disk and restores on open.

### `_AgencyStateMixin`
Subclasses provide:
- `STATE_FILE` — path under `./agency_state/`
- `_serialize_state() -> dict`
- `_deserialize_state(dict)`

…then call `_setup_autosave(*signals)` to debounce-save on input
changes (500 ms). Manual `_state_save()` also runs immediately
after result-producing events. `_state_load()` runs ~100 ms after
page construction via `QTimer.singleShot`.

| file | what's saved |
|---|---|
| `agency_state/keyword.json`    | mapia/lablog inputs, both result tables, checkboxes |
| `agency_state/morphology.json` | search keyword, top-N, analysis items, SEO titles   |
| `agency_state/image.json`      | both tabs' inputs + generated image path log        |
| `agency_state/upload.json`     | account/mode/alignment/title/body/images            |
| `agency_state/wizard.json`     | current_step + items + config + per-step inputs     |

Wizard also runs a 10-second periodic `_state_save` as a safety net.

Reset path: user deletes the JSON manually. Nothing auto-clears.

---

## 4. ma-pia.net scraping (commits `3f4e209` → `93d748e`)

Search button is `<button><span>search</span><span>조회하기</span></button>`.
The page has zero `<form>` elements; submission is JS-bound.

Working selector strategy (commit `93d748e`):
- Read button text via Selenium `.text` (descendant text), not XPath
  `text()` (direct children only).
- Priority: `조회하기` > `조회` (excluding `초기화`) > `검색`.
- Try `click()` → `execute_script(arguments[0].click())` → Ctrl+Enter
  on the textarea → a handful of conventional JS function names
  (`goSearch`, `doSearch`, `fnSearch`, …).
- After click, wait 15 s, then walk every window handle + every
  `<iframe>` looking for the largest `<table>`. Pick its `<th>` for
  headers and every non-empty `<tr><td>` for rows.
- Each table's first row is logged so a mismatched pick is obvious.

Result shape upgraded from `[{seed, related: [...]}]` to
`{seeds, headers, rows, debug}`. `_on_mapia_done` rebuilds the
`QTableWidget` with the actual column count and labels (키워드 /
월간검색수 / 합계 / 월간 블로그 발행 / …).

`send_to_lablog` auto-detects the keyword column by counting
Hangul/Latin characters per column (numeric columns score 0).

`driver.quit()` removed — chromedriver's `__del__` raises
`OSError [WinError 6]` during interpreter shutdown on Windows. The
driver is parked on `PostPro._open_drivers` so the worker returning
doesn't trigger GC. Browser stays open for the user to inspect.

Progress prints (`[Mapia] …`) at every step so the user doesn't
mistake a working session for a frozen one.

---

## 5. lablog.co.kr scraping

### Profile reuse (commit `2c41542`)
New `🔑 내 Chrome에 로그인된 계정으로 시작` checkbox in the lablog
tab. When checked on Windows, points `--user-data-dir` at
`%LOCALAPPDATA%\Google\Chrome\User Data` with
`--profile-directory=Default`. When unchecked (default), uses an
absolute `./chrome_profile` that persists between runs — first run
needs a Google login, subsequent runs stay logged in.

### Driver creation hardening (commits `aa4608e`, `6bd615d`)
- Pre-clean `SingletonLock`, `SingletonCookie`, `SingletonSocket`,
  `lockfile` inside `./chrome_profile`. Untouched for the user's
  real Chrome profile.
- Pass a `build_opts()` lambda to `make_uc_driver` instead of a
  `ChromeOptions` instance — UC consumes it on first
  `uc.Chrome(options=opts)` call and raises
  `RuntimeError: you cannot reuse the ChromeOptions object` on
  retry. The lambda lets the retry build a fresh one.
- Real exception text + targeted hints now surface in the in-app
  log (locked profile / version mismatch / permission).

### Auto-recovery (commit `8d6a394`)
When the first driver attempt against the app-managed profile fails
with `cannot connect to chrome` / `session not created` /
`DevToolsActivePort`, the script `shutil.rmtree`s the profile and
retries once. User loses their saved login but the run proceeds.

### Batch processing (commit `8d6a394`)
Spec: feed mapia-derived keywords in 5-keyword queries; every 60
keywords (=12 queries) write an Excel file and start a new batch;
stop when every keyword has been processed (no repeat passes).

```text
QUERY_SIZE = 5      # one textarea paste + one 조회 click
BATCH_SIZE = 60     # one xlsx file
```

Files land in `./agency_state/lablog_batches/lablog_batchNN_TS.xlsx`
via openpyxl, falling back to CSV if openpyxl isn't installed.
First-chunk `<th>` is cached on `self._lablog_headers` so subsequent
batches reuse the same header row.

UI: removed the `반복 횟수` spinbox (kept as hidden widget for the
existing state schema), replaced with a one-liner note.

---

## 6. Bug fixes shipped along the way

- **U+2029 SyntaxError** (commit `7d3c42f`): `selectedText()` returns
  `U+2029` (paragraph separator); embedding the literal in a string
  killed Python's tokenizer on Windows. Replaced with the `' '`
  escape.
- **chromedriver `__del__` WinError 6**: skip `driver.quit()`, park
  reference on `PostPro._open_drivers`, document that browser stays
  open.
- **`pywin32pip` typo recovery**: user double-pasted the install
  command — diagnosed and gave the corrected single-package list.
- **Python 3.14 trafilatura incompatibility**: declared optional;
  app uses BeautifulSoup as primary content extractor.
- **`distutils` missing on Python 3.12+**: documented
  `pip install --upgrade setuptools` (provides the
  `_distutils_hack`) as the fix for
  `undetected-chromedriver`'s `from distutils.version import …`.

---

## 7. Files added to the repo

```
all_in_one.py                       # main app (modified)
all_in_one_unified.txt              # snapshots for download
all_in_one_agency.txt
all_in_one_wizard.txt
all_in_one_topnav.txt
all_in_one_mapia_fix.txt
all_in_one_mapia_safe.txt
all_in_one_mapia_progress.txt
all_in_one_mapia_debug.txt
all_in_one_mapia_click.txt
all_in_one_lablog_profile.txt
all_in_one_autosave.txt
all_in_one_lablog_diag.txt
all_in_one_uc_builder.txt
all_in_one_lablog_batch.txt
agency_state/                       # runtime data (gitignore candidate)
  ├─ keyword.json
  ├─ morphology.json
  ├─ image.json
  ├─ upload.json
  ├─ wizard.json
  └─ lablog_batches/
     └─ lablog_batchNN_*.xlsx
chrome_profile/                     # selenium profile (gitignore candidate)
generated_images/                   # AI image output (gitignore candidate)
```

---

## 8. Runtime dependencies

Already installed during the session:

```text
PyQt6
undetected-chromedriver
selenium
openpyxl
pandas
youtube-transcript-api
pywin32          # Windows-only paths in upload helper
pyperclip
beautifulsoup4
requests
openai
google-genai
Pillow
feedparser
python-dotenv
setuptools       # provides distutils shim on Python 3.12+
```

Skipped:
- `trafilatura` — requires Python `<3.14`; current install is 3.14.

---

## 9. Commit list

```text
8d6a394 Lablog: 5-keyword queries, 60-keyword batches, auto Excel per batch
6bd615d Pass ChromeOptions builder lambdas so make_uc_driver can retry
aa4608e Surface lablog driver creation errors + auto-clear stale Chrome locks
6bb32c8 Auto-persist agency pages so input/results survive crashes & restarts
2c41542 Let lablog scraper reuse the user's existing Chrome profile
93d748e Match mapia 조회하기 button via descendant text + JS-call fallback
1e3cd76 Diagnose empty mapia results with structure dump + form.submit fallback
eb58ec1 Print mapia scrape progress so users see work is in flight
2906bb9 Harden mapia.net scraper against crashes and missing-result cases
3f4e209 Capture full mapia.net result table (all rows + all columns)
a41b5f9 Move 대행/후기성 sub-pages to a top category bar; enlarge wizard stepper
3d2b66c Add AgencyWizardPage: 10-step wizard for batch posting workflow
7d3c42f Fix SyntaxError from literal U+2029 in AgencyUploadPage editor helpers
7c8ff23 Add 대행/후기성 (Agency/Review) category with 4 sub-pages
3e80934 Add UnifiedCollectPage to consolidate 7+ collection pages into one
```
