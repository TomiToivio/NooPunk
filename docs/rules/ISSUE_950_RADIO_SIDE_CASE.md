# Issue #950: first optional solo UNSA side case

**Radio privacy incident** is an original NoöPunk scripted side case implemented
in `mud/nopunk_mud/campaign/engine.py`. The first mission scene bulletin
(`wait 10`) makes the optional dispatch available. The player accepts it with
`radio`, visits the University of Helsinki and uses `trace`, then returns
to the UNSA safehouse and uses `resolve protect` or `resolve disclose`.
The two decisions create different permanent consequences in the save.
`status` displays active/completed radio-case state. Old saves still load.
It is replayable via a new campaign instance, not repeatable within a saved run.

**Tabletop procedure:** At the first ten-minute scene transition, the GM offers
the technician's leaked-call dispatch. Visiting the university provides the
breach evidence automatically, with no random roll. At the safehouse the
player chooses to protect the source or file their identity. Record
`radio_protect` or `radio_disclose` as a persistent scenario consequence.
These are scenario flags, **not CWN rules or mechanical awards**; the CWN
baseline is unchanged. This quest never gates the main investigation's core
clues, and no second player, LLM, API or Mesa process is required.

Automated acceptance: `mud/tests/test_radio_sidequest_950.py`.
This is a side-case increment, not a complete single-player campaign or full
SRD port. Evennia client boot/restart tests are separate outstanding work.
