# Case: The Quiet Petition

id: story_fixture_01
start: briefing
author: Development fixture
author_reviewed: false

## Scene briefing | Europol briefing

A synthetic development scene for the story adapter. It is not Tomi's manuscript and not canon.
Romppainen receives a petition about a missing organizer and two rival groups.

- [Read the petition and event register](records) adds=missing,roster
- [Interview the witness](witness) adds=missing

## Scene records | Records desk

The register confirms attendance, not guilt. The petition names no crime yet.

- [Speak with the witness](witness) adds=witness
- [Review the message](message) adds=message
- [Return to the briefing](briefing)

## Scene witness | Witness

The witness heard an argument but cannot identify the speaker.

- [Review the message](message) adds=message
- [Recheck the records](records)

## Scene message | The message

The message asks for privacy. Its sender is not authenticated.

- [Review all leads and decide](decision) adds=message

## Scene decision | Decision

The evidence supports more than one account. Romppainen chooses what to do with it.

- [Close the case quietly](ending_private)
- [Open a formal review](ending_review)

## Scene ending_private | Private ending | ending

The organizer is not found. The file closes with an unresolved lead.

## Scene ending_review | Review ending | ending

The review finds a procedural failure. The organizer is still missing, but the case is reopened.

## Clues

- missing: A community organizer has disappeared after an argument about public disclosure.
- roster: A public event register links two rival groups to the same meeting.
- witness: A witness heard an argument but cannot identify the speaker.
- message: A message asks for privacy, but its sender cannot be authenticated.

## Hypotheses

- The groups may be connected by the same event, not necessarily by conspiracy. | requires=roster
- The disappearance could be voluntary, coercive, or staged. | requires=witness,message

## Contradictions

- roster + witness: The register lists both groups at the meeting; the witness remembers only one present. One record is wrong, or an attendance is being hidden.
