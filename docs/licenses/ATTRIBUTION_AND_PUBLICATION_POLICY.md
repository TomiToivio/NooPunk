# Attribution and licensing publication policy (issue #421)

**Status: provisional publication procedure, not a licence grant.** No software licence, content licence or commercial model is selected here. The final choices and their application belong to the author under [VISION.md](../design/VISION.md) §§7a, 9. Until recorded explicitly, the packaging policy must retain `author_decision_open: true` and a public release must fail closed.

## Separate publication surfaces

- **Software:** Author-selected OSI-approved licence for the distributable code and build tooling (including `strategy_game/` Python modules and appropriate application files). Record the exact licence identifier, copyright owners and scope in a future code-level `LICENSE` or `LICENSES/` entry; do not imply all files in this repository are covered merely by adding a root licence.
- **Original creative content:** A *separately selected* licence for original rulebook/worldbook prose, artwork and authored scenario/data records. Declare its version and applicability, distinguishing content from code, rights records and third-party licensed excerpts.
- **Mixed directories:** Use the artifact class map in [release_packaging_policy.json](../../data/licenses/release_packaging_policy.json), and a per-file exceptions manifest where needed. The blanket `strategy_game/**` software classifier must not erase its more-specific data/docs classifications. For ambiguous assets, withhold from distribution pending manual provenance review.
- **Commercial model:** Record it as a separate signed-off author decision. A no-paywalled-core/offline-reproducible requirement is already binding regardless of that model.

## Attribution procedure for every release candidate

1. Generate a distributable-file manifest and run `python tools/release_packaging_guard.py --bundle <manifest> --mode public`. The guard is a **technical precondition**, not legal clearance; an audit-mode PASS is not permission to ship.
2. For every included third-party work, record **title, author/rightsholder, source URL, exact version and licence URL/identifier, changed/adapted status, file coverage and required notices**. Put the required credit in the distributed `NOTICE` / credits file and appropriate in-game/about or rulebook copyright page. Keep authorial changes marked where required.
3. For Fate Core SRD-derived portions use the existing [Fate attribution](../../strategy_game/rpg/README.md) and exact CC BY 3.0 conditions. Do not imply the Fate logo, book art or trademark is licensed; record adaptations. The [issue #200 plan](ISSUE_200_LICENSE_AND_NOTICE_PLAN.md) contains an attribution candidate to verify at release.
4. Credit other genuinely adapted, rights-cleared works under their actual terms. **Attribution is not a substitute for permission:** no CC BY-NC-SA Eclipse Phase or Transhumanity's Fate expression, proprietary art, non-cleared OGL text or third-party logos may be smuggled into an OSI/code-plus-commercial-content bundle. Keep the quarantined EP2 prototype and adapters out, even if an audit scan passes.
5. Credit inspirations separately from actual licensed adaptations; an inspiration acknowledgement must not imply endorsement, affiliation, or that the underlying proprietary content is reusable.
6. Preserve original asset authorship and provenance in source control, record any AI-assisted generation and associated human editorial ownership policy where appropriate, and require mod authors to identify their own third-party inputs and permitted distribution terms.
7. Run human review of false-negative risk: licence-name string scans cannot detect paraphrased copyrighted expression, missing metadata, or third-party assets with no header. Document reviewer, date, release commit and outstanding exceptions before shipping.

## Author decision record (unfilled; must not be auto-populated)

| Decision | Selection | Gate |
| --- | --- | --- |
| Software licence (exact OSI identifier/version) | **NOT SELECTED** | Block public release |
| Original content licence (exact identifier/version) | **NOT SELECTED** | Block public release |
| Commercial model and distribution permissions | **NOT SELECTED** | Block release business decision |
| Publication scope / exceptional third-party permissions | **NOT CLEARED** | Block affected artifacts |

Once the author makes these decisions: update the rights ledger and packaging policy coherently, publish verified licence texts and an accurate NOTICE, implement release-manifest validation, run tests and human review, and only then change the release-gate status. Do not set `author_decision_open` to false merely to close a tracker.

**Evidence:** [#421](https://github.com/TomiToivio/NooPunk/issues/421), [PR #429](https://github.com/TomiToivio/NooPunk/pull/429), [licence/NOTICE plan](ISSUE_200_LICENSE_AND_NOTICE_PLAN.md), [release gate](ISSUE_200_CC_RELEASE_GATE.md).
