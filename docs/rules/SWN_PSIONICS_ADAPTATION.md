# SWN Revised psionics in NoöPunk

**Source:** Kevin Crawford, *Stars Without Number Revised* (2017), chapter **Psionics**, printed pp. 29–43. The user-supplied PDF provides the source for this implementation. It is copyrighted source material, not repository-redistributable content. Refer to a licensed copy for the individual powers and precise effects.

## Rules mapping

NoöPunk uses Cities Without Number as its default chassis, supplemented by the SWN Revised psychic subsystem. A psychic has six potential disciplines: **Biopsionics, Metapsionics, Precognition, Telekinesis, Telepathy, Teleportation**. Training and technique access are separate from activation and Effort accounting.

* A full SWN psychic package may train in multiple disciplines. A partial psychic is limited to one.
* Psychic disciplines are ranked 0 through 4. A technique may only be learned once its particular discipline meets the required level; its effects must be explicitly provided in a licensed or original catalogue.
* The SWN maximum Effort calculation is **1 + highest psychic skill rank + the better of Wisdom or Constitution modifiers** (with a practical minimum of one in the existing NoöPunk engine).
* Effort is **committed**, not permanently spent. Reservations are attached to an active power, a scene, or a day, and are restored when the appropriate duration ends or after rest. Reusing the same reservation key is rejected.
* SWN also describes **torching**, risky overexertion with lasting consequences. Do not silently substitute a harmless Effort refill. This remains a dedicated pending mechanic.
* Some biopsionic healing creates **System Strain**. Integration with the CWN injury/healing system is pending and must not be elided.
* Natural psionic aptitude in NoöPunk is **learnable** within its fictional setting, not confined to an inherited supernatural caste. The game's explicit psychic package still gates mechanical use.
* Telepathy (natural), psychotronic devices, and direct BCI/network communication are different interfaces. Do not grant telepathic psychic skills to a BCI user automatically.

## Implementation contracts

| Capability | Module | Status |
| --- | --- | --- |
| Six discipline names and rank checks | `src/rules/swn_psionics.py` | Existing |
| Max Effort and duration-reservation model | `src/rules/swn_psionics.py` | Existing |
| Psychic package authorization and NoöPunk scenario powers | `src/rules/psionics.py` | Existing; partial catalogue |
| Full/partial psychic advancement and learned technique prerequisites | `src/rules/swn_progression.py` | Added |
| Python regression tests for progression | `tests/test_swn_progression.py` | Added |
| Complete SWN technique catalogue and effect resolution | Not implemented | Requires licensed-source-derived mechanical specification and original wording |
| Torching, System Strain, training costs and character creation | Not implemented | Follow-up |
| Godot progression parity, UI and end-to-end scenario wiring | Not implemented | Follow-up |

The source book explains techniques, their costs, targets, activation timings and prerequisites. **The existing three original NoöPunk techniques are examples, not a replacement for the SWN catalogue.** Do not claim that full SWN psionics is playable merely because discipline progression and Effort work.

## Testing

Run `python -m unittest tests.test_swn_progression` from repository root. Full release validation must also run existing rule and Godot regression suites. No pages or technique prose from the uploaded PDF should be committed.
