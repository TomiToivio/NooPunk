# Issue #569 — full-tree similarity audit against the Without Number books

**What this is.** The rights matrix ([`ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`](ISSUE_569_WITHOUT_NUMBER_RIGHTS.md))
closed every item of #569 except one, in its own words: *"a complete repository-wide similarity audit
remains outstanding"*. This is that audit, run on **2026-10-25**, with its method, corpus fingerprints
and measured result.

It changes no file outside this record, deletes nothing, and claims no licence.

---

## 1. Why not a keyword search

The rights matrix already refuses that shortcut: a name/keyword ban *"would falsely reject legitimate
attribution and miss paraphrased copying"*. Both halves are real. A search for "Without Number" hits
this very document; a search for distinctive nouns hits our own setting vocabulary. And neither finds
a lifted sentence that changed the character names.

So the audit measures **n-gram containment**: does any file in this tree contain a run of **N
consecutive words** that also appears in a licence-blocked source? `N = 10` — long enough that a shared
run is copying rather than coincidence, short enough to catch a lifted fragment inside a longer
sentence. Normalisation is lowercase word tokens with punctuation dropped, so reformatting,
re-wrapping and case changes do not hide anything.

## 2. Two corpora, because a match is not a verdict

Four books, two licence statuses, and the distinction decides whether a hit is a problem:

| corpus | documents | status | what a hit means |
| --- | --- | --- | --- |
| **blocked** | Stars Without Number Revised (free ed., 261 pp); Ashes Without Number (free ed., 261 pp) | no SRD located, no licence statement in either file | a hit here is the thing the audit exists to catch |
| **attributable** | Cities Without Number SRD; Worlds Without Number SRD (both CC0) | CC0 — reusable with attribution | a hit that *also* occurs here is **attributable**, not a violation |

The comparison corpus is a hash set. **No third-party text is stored, printed or committed** — the
report carries our path, the line, the run length and the classification, never the matched words.

Corpus fingerprints, so a later run can prove it used the same books:

| document | sha256 |
| --- | --- |
| `StarsWithoutNumberRevised-FreeEdition-122917.pdf` | `22ef6826a5b350d66888eef386b3c7f8bf02f091c18183a241e52c3cf2f44a3f` |
| `AshesWithoutNumber_FreeVersion_071025.pdf` | `033766a846f3106b72a8f72876f4dc98d319102cfc97fc39e6b79ffa9c58d3a6` |
| CWN SRD (`CWN-SRD-V5` markdown, 65 468 unique 10-grams) | repository snapshot, 2026-10-25 |
| WWN SRD (`WWNSRDV1` markdown, 80 759 unique 10-grams) | repository snapshot, 2026-10-25 |

## 3. Result

```
$ python3 tools/audit_without_number_expression.py \
    --source StarsWithoutNumberRevised-FreeEdition-122917.pdf \
    --source AshesWithoutNumber_FreeVersion_071025.pdf \
    --cc0-source CWN-SRD-V5 --cc0-source WWNSRDV1
```

| quantity | value |
| --- | ---: |
| text files scanned (`.md .py .json .yaml .yml .gd .txt .html`, excluding `.git`/caches) | **946** |
| unique blocked-corpus 10-word runs | 373 766 |
| unique attributable-corpus 10-word runs | 138 919 |
| **first-party hits** | **0** |
| first-party blocked-only hits | **0** |
| quarantined hits | 32, all in one file |
| quarantined blocked-only hits | **0** |

**The first-party tree is clean**: no file outside the preserved corpora shares a ten-word run with
either blocked book.

### The one finding, stated precisely

`docs/archive/RULEBOOK.md` — the archived pre-#120 rulebook — contains **32** ten-word runs that also
occur in the blocked corpus. **All 32 also occur in the CC0 SRD corpus**, so they are attributable SRD
wording (the family's shared skill-level table and skill descriptions), not a copy of protected
expression. The file is additionally inside the `archive/` quarantine, which the release policy already
excludes from packaging.

Disposition: **report, do not delete**. The file is preserved history, the overlap is licence-permitted
with attribution, and the live rulebook (`RULEBOOK.md`, `rulebook/`) has **zero** hits. If a future
release ever includes the archive, those 32 runs need the CWN/WWN attribution notice — which
`docs/sources/ATTRIBUTION.md` is the place for.

## 4. Enforcement, and the honest limit

- **The corpus is not shippable.** The books are copyrighted products on the operator's disk; embedding
  their text (or a shingle fingerprint derived from it) in the repository would be the very thing this
  audit prevents. **This makes a similarity gate impossible in CI**, and the audit says so instead of
  pretending otherwise.
- **The tool is therefore an operator tool**, documented and tested (`tests/test_audit_without_number_expression.py`,
  9 code tests) so the run is reproducible by anyone holding the books.
- **The CI-side gate remains `tools/release_packaging_guard.py`** — manifest, resolved author licence,
  quarantine classes, and the `LICENSE`/`NOTICE` absence rule. It does not and cannot detect n-gram
  overlap; #569's item 4 is satisfied by the release gate plus this operator audit, and the division of
  labour is stated here rather than implied.
- **Re-run trigger:** a new edition of any book (fingerprints above change), a new SRD, or any future
  import of third-party prose. The audit is cheap: 22 seconds for 946 files against 373 k shingles.

## 5. What was not done, and why

- **No paraphrase detection.** Containment catches verbatim runs. A genuine paraphrase detector is an
  LLM-assisted similarity review; it is out of scope for an offline deterministic tool, and the rights
  matrix's own rule (human review before admitting text) remains the control that matters.
- **No archive remediation.** Deleting preserved history is forbidden by the repo's own policy
  (*"report rather than silently delete"*); the overlap is recorded instead.
- **No licence selection.** D10 stays the author's; nothing here creates `LICENSE` or `NOTICE`.

— Ai (愛)
