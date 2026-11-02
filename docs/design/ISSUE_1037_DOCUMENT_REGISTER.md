# Issue #1037 — the in-world document register (register 3 gets a mechanism)

**What this is.** Issue #1037 asks for three registers of writing; the third is *documentary /
Situationist collage* — memos, dossiers, forms, transcripts, adverts. Until now the campaign could
look, travel, talk, ask, examine and fight, but it could not **read** anything. This records the
mechanism that closes that gap without writing a single new fact.

## What was built

| Piece | Where |
| --- | --- |
| `DOCUMENTS` register | `mud/nopunk_mud/campaign/content.py` |
| `read` command and renderer | `mud/nopunk_mud/campaign/engine.py` (`_cmd_read`, `_document_body`) |
| Tests | `tests/test_document_register_1037.py` (8 tests, `unittest`) |

Two documents exist today:

- **`case_file`** — a dossier gated on the folder (`has_folder`). It prints one form line per clue
  in the case: collected clues show their canonical text, uncollected ones show `[ ] … not in the
  file`. Refusal names what is missing, as every refusal in this engine does.
- **`activity_log`** — a form that prints the consequences the engine has actually recorded
  (`insufficient_evidence`, `fled_encounter`, `radio_protect`, …), each with the deadpan
  "no countersignature on record".

## The rule that keeps this honest

**A document renders canon; it never authors it.** Every body line is either a `content.CLUES`
text or a blank-form marker; the activity log is `state.consequences` verbatim. There is no
narrative prose in `DOCUMENTS` beyond the form's own furniture (`kind`, `issuer`, `footer`) — the
dull institutional words a form carries anyway.

That constraint is the point, not a shortcut:

- it means the register cannot quietly become a second canon store, which is the failure mode the
  repo already guards against for rules engines;
- adding a genuinely authored document later is a **writing** decision that needs no engine change:
  a new entry with a `source` the renderer knows, or a new `source` that reads an existing data
  file;
- the tests assert the constraint (`test_the_document_adds_no_text_of_its_own`), so a future agent
  cannot smuggle invented lore in through the renderer.

## What this is *not*

- It is not the first episode. Which story opens the shared canon is an author decision (`D70`).
- It is not a canon cross-reference layer between prose and Evennia scenes. That is the second
  missing piece in #1037 and it needs an authored episode to point *at* before a format is worth
  fixing.
- It does not touch the rules: no CWN/SWN mechanic, no skill, no stat. `read` is a view.

## Smallest next step, when the author wants it

One authored fragment — a memo, an advert, a leaked transcript, 200–800 words — dropped into
`data/` with an id, and one `source` branch in the renderer that prints it once the player is in the
right place with the right flag. That is the whole seam: the register already carries it.
