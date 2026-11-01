# From two catalogues to one canonical string per key (#996)

Under #996 the MUD has **one canonical language** and no localizations. The current string layer still speaks
in the language of the policy it replaces. This is the audit and the migration plan, and the reason the
migration is safe.

## What exists now

`mud/nopunk_mud/i18n.py`:

| Element | Current meaning | Problem under #996 |
| --- | --- | --- |
| `LOCALES = ("fi", "en")` | two supported locales | implies two editions of the game |
| `DEFAULT_LOCALE = "fi"` | the game plays in Finnish | there is no locale to select |
| `FALLBACK_LOCALE = "en"` | missing Finnish falls back to English | reads as translation, not provenance |
| `Translator(locale=...)` | per-player language | a player cannot choose a language |
| `pending_finnish()` | translation backlog | measures a deliverable that no longer exists |

`locale/en.json` holds ten agent-written strings; `locale/fi.json` holds the same keys as `null`. None of these
strings is player-visible yet: nothing outside tests calls the translator.

## Why migration cannot break saves

Saves carry **identifiers, not prose**. `solo_campaign.Campaign.to_dict()` persists exactly `stage`, `clues`
and `completed`; `world_state.WorldState.save()` writes the state snapshot. Scene text lives in Python
(`solo_campaign.SCENES`, `campaign/content.py`) and is never serialised into a save.

Two consequences follow, and they are the whole safety argument:

1. **Changing how a key resolves cannot corrupt an existing save**, because the save never stored the
   resolution. A old save re-opened after the migration reads the same ids and re-derives text.
2. **Nothing must be deleted to migrate.** The old catalogues stay readable as provenance while the canonical
   layer is introduced beside them. Tomi's authored text is never rewritten by a schema change.

The one real risk is a *silent text change*: if a key's canonical string is replaced, a player returning to an
in-progress scene sees different words for a scene they already read. That is a content decision, not a
mechanical one — so the migration changes where text is resolved from, never what the text says.

## Target shape

One canonical string per key, with the two old catalogues demoted to **provenance**:

```
key                     canonical (player-visible Finglish)
  ├── en.json   → agent-written source        (provenance: who wrote it, and in what)
  └── fi.json   → Tomi-authored text, if any  (read-only; never machine-modified)
```

Resolution becomes: **canonical if present; else the agent source; never a translation between them.** That is
already close to what `Translator.text()` does, which is why the change is mostly naming and framing rather
than logic.

## Steps

1. **Rename the semantics, keep the API shape.** Document `fi` as the author layer and `en` as the source
   layer; remove the idea that a player selects a locale. Keep `LOCALES` as a provenance tuple for now so
   existing call sites and tests keep working.
2. **Add the canonical accessor.** A single function that returns the one string for a key, without a locale
   argument, used by all new player-facing code.
3. **Migrate call sites one scene at a time**, as #984's wiring note already requires. New code must not call
   the locale-taking path.
4. **Retire the translation vocabulary.** `pending_finnish()` measures nothing real once there is no Finnish
   edition; replace it with a provenance report ("how many keys are Tomi-authored, how many agent-written").
5. **Keep `locale/*.json` readable** until every call site is migrated, then fold the canonical strings into a
   single `canonical.json` **without deleting** either source file.

Nothing in this plan is urgent enough to do all at once, and step 3 is deliberately per-scene: a bulk rewrite
of player-facing text is exactly the "silent translation" #996 forbids.

## Non-goals

- No translation service, no machine translation, no `translate()` call anywhere.
- No deletion of Tomi-authored text, and no rewriting of it to smooth the schema.
- No player-facing language switcher. There is one language.
- No Concordia dependency. Every step above works with no LLM.
