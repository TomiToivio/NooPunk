# NoöPunk Simulator Python Code

**Designated home for Python implementations of Simulator Rulebook mechanics.** Follow [issue #1309](https://github.com/TomiToivio/NooPunk/issues/1309).

**Current canonical implementation is still [`../../src/social_sim/`](../../src/social_sim/)** (`kernel.py`, `ai26.py`). This directory is a scaffold, not an independent engine. **Do not copy or reimplement that kernel here.** Move code here only under an explicitly scoped migration with compatibility imports, tests and preserved reproducibility. Each future rule/schema change must have a synchronized human-readable Rulebook update.

Implement incrementally: Social Graph → Ideology projection/DNA bridge → Helsinki Physical Graph. Keep Python core headless and independent of Streamlit or CWN; preserve observed/inferred/synthesized/simulated distinctions. Agents must not edit `../Paper/`.
