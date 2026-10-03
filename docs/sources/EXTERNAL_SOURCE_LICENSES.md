# External source license audit (issue #60)

What may later be imported into NoöPunk from the sources issue #60 names, and under
what terms. This is the check that `EP2_HOME_BREW_SOURCES.md` records as not yet done:
*"These external projects are references only until their individual licenses and
provenance have been checked."*

Machine-readable record: [`data/sources/external_sources.json`](../../data/sources/external_sources.json).
Every finding below is a dated real-world observation, not in-world canon.

**Nothing has been imported.** No third-party code, data or text is present in the
working tree or anywhere in the repository history. This document exists so that a
later import is a decision rather than an accident.

## The governing license

Unless noted otherwise, Eclipse Phase releases by **Posthuman Studios** are
**CC BY-NC-SA 4.0** — verified from the publisher's page on 2026-10-03. Three
conditions bind anything derived from EP material:

1. **noncommercial** only;
2. **attribution** to Posthuman Studios, LLC, with a link to https://eclipsephase.com;
3. **ShareAlike** — derivatives under the same license.

The page also explicitly encourages fan fiction, campaign websites, house rules,
netbooks and crossover systems. NoöPunk is inside the use case the publisher names.

The condition that actually constrains the codebase is **ShareAlike**: any *file* that
mixes EP expression into NoöPunk content becomes CC BY-NC-SA as a whole. A permissive
license cannot cover the mixture, so the EP-derived boundary has to stay visible in the
file layout rather than in a README sentence.

## Findings

| Source | License | Can we import? |
| --- | --- | --- |
| EP2 online rules (`eclipsephase.github.io`) | CC BY-NC-SA 4.0 | **Yes**, EP-derived |
| EP2 Quick-Start Rules (PDF) | CC BY-NC-SA 4.0 | **Yes**, EP-derived — but do not commit the PDF |
| Artemystra/eclipsephase | CC BY-NC-SA (README says 3.0) | **Yes**, EP-derived — with care |
| `ralfbiedert/eclipse-phase-2-tools` | **none found** | **No** |
| Eclipse Helper character generator | split / hedged | **No** |
| PbtA conversion site | **unverified** (HTTP 403) | **No** |
| Rob Boyle's EP1 PDF index | publisher's CC BY-NC-SA | **Yes**, EP-derived — index only, don't rehost |
| Transhumanity's Fate, Fate Core, NCO, 2E Morphs | not established | **Not present on disk** |

### EP2 online rules — importable, EP-derived

`https://eclipsephase.github.io/en/01/00-infamy.html`. The repository carries a `LICENSE`
file with the full CC BY-NC-SA 4.0 legal text. Two details worth recording because both
mislead a casual reader:

- GitHub's license API reports this repository as **`NOASSERTION` ("Other")**. That
  under-reports it — the LICENSE file is standard CC BY-NC-SA 4.0, read directly.
- The repository's description says *"Tradução para Português"*. It nonetheless serves
  both `docs/en/` and `docs/pt_br/`, so the **English** rules URL the issue names is
  served from this repository. The Portuguese description is not a reason to distrust
  the English path.

Use compact rule summaries and structured data. The issue forbids mirroring rulebook
prose, and that constraint matters more here than the license does.

### EP2 Quick-Start Rules — importable, do not commit the PDF

An official Posthuman Studios release, so the publisher's general statement covers it.
Read it for the minimum viable rules kernel. The PDF is **not** in this repository and
must not be added — it is a hosted third-party file, and the issue says not to commit
third-party PDFs unless redistribution is explicitly permitted. Confirmed: no `.pdf`
exists in the working tree or anywhere in the repository history.

### Artemystra/eclipsephase — importable, with two cautions

A FoundryVTT system with character data, ware, morphs, traits and gear. Its README
"Legal" section declares the rules and non-registered trademarks to be CC BY-NC-SA and
states this *"is also true for any additions made or code written by the developer"*.

Cautions:

- There is **no LICENSE file**; the only license evidence is README prose.
- That prose cites the **3.0** license URL while current EP releases are **4.0**. Record
  both and prefer the stricter reading.
- The site uses EP logos and trademarks *"with their permission"* — a permission granted
  to **that project** does not transfer to NooPunk.

Import dataset by dataset with provenance per dataset. Never wholesale.

### `ralfbiedert/eclipse-phase-2-tools` — do not import

No LICENSE file, no license statement anywhere in the repository, and the GitHub license
API reports `NONE`. **Absent a grant, no code or data may be copied from it.** The README
is a download page linking Excel and PDF tools on OneDrive and has no license section at
all.

The issue anticipates this: *"Even when code is not directly reused, its architecture may
be useful as implementation reference."* Reading it for architecture is fine. Copying is
not.

### Eclipse Helper — do not import (the author's own suggestion, checked)

Added in the issue thread as a character-generation reference. Its terms are split, so
neither half is clean:

- the site footer says the data and text come from the Eclipse Phase books under
  CC BY-NC-SA 4.0;
- the site's own code is *"the same license where possible (libraries are under their own
  licenses)"* — a hedge, not a grant;
- both backing repositories, `Arokha/EP2-Data` and `Arokha/ep2-helper`, report **no
  license**.

So: useful to **read** as a comparison for EP2 character-creation flow — backgrounds,
careers, aptitudes, morph selection, traits, pool values, build validation — which is what
the thread asks for. Do not scrape its data. The MIT-licensed library it bundles is a
third-party dependency and does not license the generator.

### PbtA conversion — unverified, so no import and no claim

`https://eclipse-phase-apocalypse.obsidianportal.com/wikis/main-page` returned **HTTP 403**
with no content read. This is recorded as a **blocked verification, not a negative
result**: nothing is known about its terms, and nothing may be asserted about them. It
stays a design-comparison candidate, and the issue already says not to switch to it
wholesale.

### Rob Boyle's EP1 PDF index — an index, not a grant

`https://robboyle.wordpress.com/eclipse-phase-pdfs/` links to official EP releases rather
than hosting them; the linked PDFs carry the publisher's license. The page itself grants
nothing, and copying the linked PDFs into this repository would redistribute
third-party-hosted files.

### The attached conversions are not present

The issue names Transhumanity's Fate, Fate Core, the Neon City Overdrive conversion and the
2E Morphs and Traits conversion as attached files. **None of them exists** in the
repository or anywhere on this machine. Their terms cannot be recorded because the material
is absent.

If they are supplied, each needs its own entry before any content is used. In particular:
**Fate Core is published by Evil Hat Productions under its own Creative Commons terms,
which are not Eclipse Phase's.** The two EP conversions are community works of unknown
terms. Assume none of them is importable until checked.

## What this means for the codebase

- **EP-derived paths:** `src/eclipse_phase_homebrew/`, `src/concordia_runtime/ep2_adapter.py`.
  Both are marked in `docs/licenses/ECLIPSE_PHASE_HOMEBREW.md`.
- **NoöPunk-original material** stays separate unless a file explicitly says otherwise.
- **Noncommercial:** while any file mixes in EP-derived material, the project is
  noncommercial. Commercial use would require strictly separating NoöPunk's own content.
- **ShareAlike:** do not relicense EP-derived text, code or data under an incompatible
  license.

## The current implementation is a reimplementation, not a copy

The initial #60 kernel is a compact reimplementation of public EP2 rules *concepts* —
percentile roll-under tests, the 33/66 superior-result rule, critical doubles, defaulting,
the ±60 modifier cap, and the common pool spend options — rather than copied rulebook
prose. No PDF, no third-party dataset and no third-party source file is present.

This matters for ShareAlike: implementing a described mechanic is not the same act as
copying the expression of it, and the project's stated aim is *"to implement and transform
the rules, not to mirror the Eclipse Phase books."*
