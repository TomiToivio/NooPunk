# #950: Mission time in the solo UNSA case

The headless `CampaignEngine` (and the Evennia `solo` command that wraps it) now
accepts `wait <minutes>` with whole minutes 1–60. `status` reports mission minute
and the zero-based 10-minute scene index. The first scene transition emits a
one-time UNSA radio bulletin that is recorded in the persistent campaign flags.
Radio intelligence is **not** evidence; core clues remain guaranteed when examined.

This is an incremental application of the established CWN mission clock durations,
not a new CWN action or an alternative dice mechanic. Command turns and elapsed
mission minutes remain distinct; other commands currently do **not** spend time,
and per-scene powers, pursuit, sleep, and timed encounter consequences are not
implemented here. Older saves lacking `minute` load at minute zero; negative
clock values are rejected.

Tests: `mud/tests/test_solo_mission_clock_950.py`. Tabletop parity: in a
human-run game, the referee records elapsed mission minutes and announces the
optional radio scene once when the first ten minutes elapse. This campaign
fiction is a **NoöPunk scenario event**, not a rule from the CWN SRD.

Issue #950 remains a larger roadmap: this does not complete the campaign,
the SRD port, or the required Evennia live-client acceptance test.
