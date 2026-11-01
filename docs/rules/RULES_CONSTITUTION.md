# The rules constitution

**Status: permanently locked by the author (#1006).** This is not a design proposal. It exists to end a cycle:
the core mechanics have been revisited repeatedly, and each revisit cost more than it bought.

## The foundation

**NoöPunk's OSR base is Cities Without Number (CWN)**, with **Stars Without Number (SWN)**, **Ashes Without
Number (AWN)** and **Worlds Without Number (WWN)** as the compatible source family.

**Minimum playable system: vanilla CWN + SWN psionics.** Nothing smaller is a NoöPunk game; nothing larger is
required to begin.

## Precedence

1. **CWN** — authoritative core. Where sources disagree, CWN wins.
2. **SWN** — the essential companion module: psionics, because NoöPunk's PSI premise needs it.
3. **WWN**, **AWN** — optional scoped extensions, imported deliberately and named as mods.

## What is locked

Preserve CWN **verbatim in behaviour**: the six core attributes, the skill list and its definitions, skill
levels and advancement, character creation, combat, saves, equipment procedures, and the fundamental
resolution rules.

## What is forbidden

- **Do not redesign** the core.
- **Do not replace** attributes or rewrite skill mechanics.
- **Do not simplify** a rule because it looks heavy.
- **Do not silently alter** behaviour while porting.
- **Do not fork** a rule into a mod so the core can stay "clean" — a second copy of a rounding rule is how a
  rule drifts.

## How NoöPunk is built on top

NoöPunk modules — Noösphere, Psyche, ontological shock, ideology, reputation, investigative procedure — are
**layers on the vanilla foundation**, never replacements for it. A mod may add procedures, tables and
resources. A mod may not redefine how a skill check, a save, or damage resolves.

Cross-system bridging (SWN psionics into a CWN character, for instance) must be **specified separately** and
visibly, in its own document, rather than blended into a port until nobody can say which game a number came
from.

## The machine record

`data/rules/rules_constitution.json` carries the same decision in a form tests can enforce. If the two ever
disagree, this document is the authority and the JSON is the bug.
