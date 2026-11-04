# NoöPunk paradigm-shift source monitoring (#1144)

**Source of truth for monitoring policy:** [Timeline Watch Monitoring Protocol](../../rulebook/7_TIMELINE.md). **Source of truth for fiction:** [TIMELINE.md](../../TIMELINE.md). This document does not replace either.

**Machine-readable candidates:** [monitoring_registry.json](../../data/sources/monitoring_registry.json). These sources are *curated discovery leads*, not automatically factual, canonical, current, or subscribed. All 45 entries are initially `unverified`, including the three user-provided videos. `feed_url: null` means **not yet being polled**. The playlist and show page URLs are not necessarily RSS feeds.

## Workflow

1. Verify a publisher's official show/channel identity, item metadata, activity, permissions and RSS/Atom URL. Record a genuine HTTPS feed in `feed_url`, set `status: active`, and document provenance. Set `archival` for a discontinued show. Never invent feed URLs.
2. Read existing new-item reports from LaclauGPT and PCM first. Do not build a second Timeline Watch scheduler. The existing scheduled Timeline Watch can consume this registry in its source-discovery stage; repository files alone do **not** change the external scheduler.
3. Inspect the registry: `python3 tools/poll_monitoring_sources.py --dry-run`. Poll verified feeds: `python3 tools/poll_monitoring_sources.py --state .cache/monitoring_seen.json`. Run from the repository root. Save the state file persistently between runs (ignore generated cache in version control).
4. This tool fetches **RSS/Atom metadata only**, with HTTPS feeds, a size cap and network timeout. Unavailable/deleted feeds log an error without stopping other feeds. It returns JSON of newly discovered items with source URL, date when supplied, `evidence_level=source_statement` and `canon_status=review_required`; a missing date remains null, never silently interpreted as today. No transcript copying, no claim verification, no lore insertion.
5. The existing Timeline Watch makes editorial relevance, corroboration, novelty and notification decisions under the **seven-step evidence ladder** in `rulebook/7_TIMELINE.md`. Do not notify about archive backfill or generic chatter. The RSS utility does not itself publish alerts or reports.
6. Run `python3 -m unittest discover -s tests -p 'test_source_monitoring_1144.py' -v` before changing the registry/poller. The registry permits multiple shows to share the same directory URL but requires unique source IDs; items deduplicate by canonical URL and fall back to source-qualified IDs. Existing publication dates are preserved without synthesis.

### Priority cadence (for the existing watch to schedule, not new timers)

- P0: daily metadata check; P1: weekly; P2: monthly/on-demand.
- No feed is polled until a valid, verified feed URL is explicitly added.
- Downstream alerts only for **genuinely new, material developments**; do not mistake popular stories or familiar claims for a paradigm shift.
- Source evidence, reported testimony, interpretation and proposed fictional canon are distinct. No automatic changes to TIMELINE.md, City/World source documents, factions, rules or the campaign.

### Special author provenance

**Tony German**, the player-character name, is a deliberate homage to **Toni Jerrman**, whom the author interviewed for *Kulttuurivihkot*. Keep this author-supplied naming provenance separate from podcast discovery and from in-universe character biography. The Finnish science-fiction magazine **Tähtivaeltaja** is especially relevant to literary and cultural monitoring.

### Scope and known limits

Only the source *registry* and a conservative reusable polling adapter are delivered by #1144. No verified RSS endpoints, runtime scheduler changes, automatic Spotify/YouTube API integrations, transcript ingestion, or active notifications are claimed here. Direct YouTube video URLs are preserved as `platform_ids.youtube_video` and remain metadata-unverified until checked. Historical episodes can be researched manually without generating fake fresh-news alerts. Source links and research claims require verification before citations in published worldbuilding.
