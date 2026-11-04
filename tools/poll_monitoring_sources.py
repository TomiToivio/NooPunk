"""Read the NoöPunk monitoring registry and poll *verified* RSS/Atom feeds.

No scheduler is created here: Timeline Watch owns scheduling and editorial decisions.
Requires only Python's standard library. Run with --dry-run to inspect sources.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

REGISTRY = Path(__file__).resolve().parents[1] / "data/sources/monitoring_registry.json"
ATOM = "{http://www.w3.org/2005/Atom}"
TRACKING = {"fbclid", "gclid", "ref", "source"}


def canonical_url(url: str) -> str:
    if not url:
        return ""
    p = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(p.query) if k.lower() not in TRACKING and not k.lower().startswith("utm_")]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/") or "/", urlencode(query), ""))


def validate_registry(registry: dict) -> list[str]:
    errors, ids = [], set()
    for source in registry.get("sources", []):
        ident = source.get("id")
        if not ident or ident in ids:
            errors.append("missing or duplicate source id: " + repr(ident))
        ids.add(ident)
        if source.get("priority") not in {"P0", "P1", "P2"}:
            errors.append("invalid priority: " + repr(ident))
        url = source.get("canonical_url")
        if url is not None and urlsplit(url).scheme != "https":
            errors.append("not an HTTPS source URL: " + repr(ident))
        feed = source.get("feed_url")
        if feed and urlsplit(feed).scheme != "https":
            errors.append("not an HTTPS feed: " + repr(ident))
        if source.get("status") not in {"active", "archival", "unverified"}:
            errors.append("invalid status: " + repr(ident))
    return errors


def parse_feed(content: bytes, source_id: str) -> list[dict]:
    root = ET.fromstring(content)
    items = []
    if root.tag == "rss" or root.tag.lower().endswith("rss"):
        for item in root.findall("./channel/item"):
            items.append({"title": item.findtext("title") or "", "url": item.findtext("link") or "", "published": item.findtext("pubDate"), "id": item.findtext("guid") or item.findtext("link")})
    elif root.tag == ATOM + "feed":
        for entry in root.findall(ATOM + "entry"):
            link = next((node.get("href") for node in entry.findall(ATOM + "link") if node.get("rel") in (None, "alternate")), "")
            items.append({"title": entry.findtext(ATOM + "title") or "", "url": link, "published": entry.findtext(ATOM + "published") or entry.findtext(ATOM + "updated"), "id": entry.findtext(ATOM + "id") or link})
    else:
        raise ValueError("Not an RSS or Atom feed")
    for item in items:
        item["source_id"] = source_id
        item["canonical_url"] = canonical_url(item["url"])
        item["evidence_level"] = "source_statement"
        item["canon_status"] = "review_required"
    return items


def unique_items(items: list[dict], seen: set[str] | None = None) -> list[dict]:
    seen = set() if seen is None else seen
    result = []
    for item in items:
        key = item.get("canonical_url") or str(item.get("source_id", "")) + ":" + str(item.get("id", ""))
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--dry-run", action="store_true", help="show registry readiness without network requests")
    parser.add_argument("--state", type=Path, help="persistent JSON state path for already-seen item keys")
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args(argv)
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    errors = validate_registry(registry)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2
    if args.dry_run:
        print(json.dumps({"sources": len(registry["sources"]), "verified_feeds": sum(bool(s.get("feed_url")) and s.get("status") == "active" for s in registry["sources"]), "unverified": sum(s["status"] == "unverified" for s in registry["sources"])}, indent=2))
        return 0
    seen = set(json.loads(args.state.read_text(encoding="utf-8"))) if args.state and args.state.exists() else set()
    new = []
    for source in registry["sources"]:
        if source["status"] != "active" or not source.get("feed_url"):
            continue
        try:
            request = urllib.request.Request(source["feed_url"], headers={"User-Agent": "NooPunkTimelineWatch/1.0"})
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                items = parse_feed(response.read(2_000_000), source["id"])
            new.extend(unique_items(items, seen))
        except (OSError, ET.ParseError, ValueError) as exc:
            print(f"Feed unavailable ({source['id']}): {exc}", file=sys.stderr)
    # Caller must supply a durable state path to enable de-duplication between runs.
    if args.state:
        args.state.parent.mkdir(parents=True, exist_ok=True)
        args.state.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(new, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
