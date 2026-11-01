# Design workflow and language policy — manual compliance check (#989, #992)

**This is a review checklist, not a test.** AGENTS.md's *Automated tests policy: executable code only* prohibits
text-matching assertions, documentation gates and CI steps for wording, design principles and rulebook
structure: the author reviews those editorially, and they are not code contracts. So the checks below are
performed by a human or an agent during review, with the commands shown so the result is reproducible rather
than a claim.

Run them from the repository root.

---

## 1. The design workflow is reachable and singular

```bash
head -5 AGENTS.md                     # must open with DESIGN WORKFLOW and link design/README.md
grep -n "design/README.md" AGENTS.md design/README.md
```

- [ ] The **first** top-level section of `AGENTS.md` is the design workflow and links `design/README.md`.
- [ ] `design/README.md` is still the definition — `AGENTS.md` defers the document types to it rather than
      restating them. Two copies of the ten document types is two authorities, and they drift.
- [ ] No other file restates the three steps *without* linking `design/README.md`. A summary that links back
      is how an agent finds the source and is fine.

```bash
grep -rl "design document" --include="*.md" . | grep -v "^./legacy/" \
  | xargs grep -l "agents implement" 2>/dev/null
```

## 2. Day and Storyline have not been collapsed

```bash
sed -n '/## Document Types/,/## Guidelines/p' design/README.md
```

- [ ] **Day** is described as firing on world time, regardless of player progress; no Day document means no
      *special* event that day.
- [ ] **Storyline** is described as progression-gated.
- [ ] **Mission** (authored, scripted) is still distinguished from **Missions** (side content, some
      repeatable or procedural), and from **Encounters**/**Events** (random, off the main arc).
- [ ] **Location** is still three levels: Helsinki → UNSA HQ → Dr. Romppainen's Office.

## 3. The language boundary (#992) says what it means

The rule is a **scope**, not a blanket prohibition: player-visible MUD text is English-dominant Finglish;
everything else is plain English.

```bash
grep -n -iE "english only|only english|only write english" \
  AGENTS.md mud/AGENTS.md design/README.md docs/FINNISH.md docs/world/HELSINKI_SLANG_GLOSSARY.md
```

- [ ] That grep returns **nothing**. An unqualified "agents write English only" contradicts #992.
- [ ] `docs/FINNISH.md` states the player-visible scope explicitly and names the non-player-facing surfaces
      (docs, rulebooks, design documents, code, internal prompts, issue text).
- [ ] Nobody claims Concordia/LLM GM or NPC support **exists**. It is described as future work with a
      player-facing output contract, and the solo campaign stays runnable without it (#950).
- [ ] Tomi-authored Finnish/Finglish is described as **preserved verbatim** — never translated, normalised,
      corrected or overwritten — and the glossary refuses to present agent phrasing as authentic slang.
- [ ] Nadsat is cited as a *technique* (Russian loanwords), not as permission to reuse Burgess's invented
      lexicon.

## 4. The boundaries still point at one authority

```bash
grep -n -iE "cities without number|evennia|design/README.md|docs/FINNISH.md" AGENTS.md | head
```

- [ ] CWN is still the locked rules foundation (#897).
- [ ] The Python Evennia MUD in `mud/` is still the runtime, with Godot maintenance-only (#950).
- [ ] Each policy has exactly one canonical document; the others link to it.

---

## Known tension, resolved this way

#989 asked for tests *or* a clear manual compliance check. The automated-tests policy above forbids the first
for wording and design principles, so the second is what exists — this file. If a future change wants the
checks executable, it has to change that policy first, deliberately, rather than reintroduce a documentation
gate under a new name.
