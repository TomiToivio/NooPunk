# Example: Act I procurement case (authored records)

Files in the authoring format proposed by
[`docs/design/DRAFT_GRAPH_SCENES_1164.md`](../../../design/DRAFT_GRAPH_SCENES_1164.md) §11, with the same `id`/`kind`
conventions:

| file | record |
|---|---|
| [`series_europol01.md`](series_europol01.md) | series |
| [`episode_invoice.md`](episode_invoice.md) | episode |
| [`scene_invoice_interview.md`](scene_invoice_interview.md) | scene |
| [`helsinki_physical.md`](helsinki_physical.md) | physical nodes, edges and two cross-layer links |

They demonstrate the authoring format, not game content; nothing loads them.

Two invariants are visible in the files themselves:

* the two **core** leads are granted for competence plus declared access and inquiry, so a bad roll costs time,
  trust and money — never the case (`scene_invoice_interview.md`);
* every node that depends on a contested fact carries a **`source_claim`** naming the conflict — the home in
  Sörnäinen versus Kurvi company housing, and the Europol HQ address — so the author decides rather than an agent
  (`helsinki_physical.md`).
