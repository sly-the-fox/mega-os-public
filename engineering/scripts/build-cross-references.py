#!/usr/bin/env python3
"""Build core/indexes/cross-references.json — an inverted index of entity mentions.

Extracts entities (contacts, products, agents, decisions, risks, improvements, audits)
from their canonical sources, then scans all non-archived markdown files to find
cross-references. Zero API cost.
"""

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT = ROOT / "core" / "indexes" / "cross-references.json"

# Directories to exclude from scanning
EXCLUDE_DIRS = {"archive", "node_modules", ".git", ".obsidian", ".claude"}


def extract_contacts() -> list[dict]:
    """Extract contact names from business/network/contacts.md People table."""
    contacts_file = ROOT / "business" / "network" / "contacts.md"
    if not contacts_file.exists():
        return []

    entities = []
    in_people_table = False
    header_seen = False

    for line in contacts_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if stripped.startswith("## People"):
            in_people_table = True
            continue

        if in_people_table and stripped.startswith("## "):
            # Next section — stop parsing People table
            in_people_table = False
            continue

        if not in_people_table:
            continue

        if not stripped.startswith("|"):
            continue

        # Skip header row and separator
        if "Name" in stripped and "Platform" in stripped:
            header_seen = True
            continue
        if stripped.startswith("|---") or stripped.startswith("| ---"):
            continue
        if not header_seen:
            continue

        # Parse first column (Name)
        cols = [c.strip() for c in stripped.split("|")]
        # cols[0] is empty (before first |), cols[1] is Name
        if len(cols) >= 2 and cols[1]:
            name = cols[1].strip()
            if name and name != "—" and name != "Name":
                entities.append({
                    "type": "contact",
                    "name": name,
                    "canonical_file": "business/network/contacts.md",
                })

    # Also parse Declined table
    in_declined = False
    header_seen = False
    for line in contacts_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if "Declined" in stripped and stripped.startswith("## "):
            in_declined = True
            continue
        if in_declined and stripped.startswith("## "):
            in_declined = False
            continue
        if not in_declined or not stripped.startswith("|"):
            continue
        if "Name" in stripped:
            header_seen = True
            continue
        if stripped.startswith("|---"):
            continue
        if not header_seen:
            continue
        cols = [c.strip() for c in stripped.split("|")]
        if len(cols) >= 2 and cols[1] and cols[1] != "—":
            entities.append({
                "type": "contact",
                "name": cols[1].strip(),
                "canonical_file": "business/network/contacts.md",
            })

    return entities


def extract_products() -> list[dict]:
    """Extract product names from products/ subdirectories."""
    products_dir = ROOT / "products"
    if not products_dir.exists():
        return []

    entities = []
    for d in sorted(products_dir.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            entities.append({
                "type": "product",
                "name": d.name,
                "canonical_file": f"products/{d.name}/",
            })
    return entities


def extract_agents() -> list[dict]:
    """Extract agent names from .claude/agents/REGISTRY.md."""
    registry = ROOT / ".claude" / "agents" / "REGISTRY.md"
    if not registry.exists():
        return []

    entities = []
    in_table = False
    for line in registry.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "Agent" in stripped and "Category" in stripped:
            in_table = True
            continue
        if stripped.startswith("|---"):
            continue
        if not in_table or not stripped.startswith("|"):
            if in_table and not stripped.startswith("|"):
                in_table = False
            continue
        cols = [c.strip() for c in stripped.split("|")]
        if len(cols) >= 2 and cols[1]:
            name = cols[1].strip().replace("`", "")
            if name and name != "Agent":
                entities.append({
                    "type": "agent",
                    "name": name,
                    "canonical_file": ".claude/agents/REGISTRY.md",
                })
    return entities


def extract_ids(filepath: str, pattern: str, entity_type: str) -> list[dict]:
    """Extract ID-based entities (DEC-001, R-006, IMP-001, AUD-001) from a file."""
    fpath = ROOT / filepath
    if not fpath.exists():
        return []

    entities = []
    seen = set()
    for match in re.finditer(pattern, fpath.read_text(encoding="utf-8")):
        entity_id = match.group(0)
        if entity_id not in seen:
            seen.add(entity_id)
            entities.append({
                "type": entity_type,
                "name": entity_id,
                "canonical_file": filepath,
            })
    return entities


def collect_all_entities() -> list[dict]:
    """Collect all entities from canonical sources."""
    entities = []
    entities.extend(extract_contacts())
    entities.extend(extract_products())
    entities.extend(extract_agents())
    entities.extend(extract_ids("core/history/decisions.md", r"DEC-\d+", "decision"))
    entities.extend(extract_ids("active/risks.md", r"R-\d+", "risk"))
    entities.extend(extract_ids("active/improvements.md", r"IMP-\d+", "improvement"))
    entities.extend(extract_ids("active/audits.md", r"AUD-\d+", "audit"))
    return entities


def collect_scan_files() -> list[Path]:
    """Collect all markdown files to scan, excluding archive and hidden dirs."""
    files = []
    for md_file in ROOT.rglob("*.md"):
        # Check if any parent directory is in the exclude list
        rel = md_file.relative_to(ROOT)
        parts = rel.parts
        if any(part in EXCLUDE_DIRS for part in parts):
            continue
        files.append(md_file)
    return sorted(files)


def build_cross_references() -> dict:
    """Build the inverted index."""
    start = time.monotonic()

    entities = collect_all_entities()
    scan_files = collect_scan_files()

    # Build regex patterns for each entity
    entity_patterns = []
    for entity in entities:
        name = entity["name"]
        escaped = re.escape(name)
        # For short IDs (R-001, DEC-001), use exact match
        # For names (contacts, products), use word boundaries
        if re.match(r"^[A-Z]+-\d+$", name):
            pattern = re.compile(escaped)
        elif re.match(r"^[a-z]", name):
            # Product names or agent names — case-sensitive word boundary
            pattern = re.compile(r"\b" + escaped + r"\b")
        else:
            # Contact names — case-sensitive word boundary
            pattern = re.compile(r"\b" + escaped + r"\b")
        entity_patterns.append((entity, pattern))

    # Scan all files
    results = {}
    total_mentions = 0

    for entity, pattern in entity_patterns:
        key = f"{entity['type']}:{entity['name']}"
        referenced_in = []
        mention_count = 0

        for md_file in scan_files:
            try:
                content = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            matches = pattern.findall(content)
            if matches:
                rel_path = str(md_file.relative_to(ROOT))
                referenced_in.append(rel_path)
                mention_count += len(matches)

        if referenced_in:
            results[key] = {
                "type": entity["type"],
                "name": entity["name"],
                "canonical_file": entity["canonical_file"],
                "referenced_in": referenced_in,
                "mention_count": mention_count,
            }
            total_mentions += mention_count

    duration_ms = int((time.monotonic() - start) * 1000)

    return {
        "version": 1,
        "generated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "entity_types": ["contact", "product", "agent", "decision", "risk", "improvement", "audit"],
        "entities": results,
        "stats": {
            "total_entities": len(results),
            "total_mentions": total_mentions,
            "files_scanned": len(scan_files),
            "scan_duration_ms": duration_ms,
        },
    }


def main():
    index = build_cross_references()

    # Atomic write
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
    tmp.rename(OUTPUT)

    stats = index["stats"]
    print(
        f"Built cross-references: {stats['total_entities']} entities, "
        f"{stats['total_mentions']} mentions across {stats['files_scanned']} files "
        f"in {stats['scan_duration_ms']}ms"
    )

    # Show top entities by mention count
    sorted_entities = sorted(
        index["entities"].values(), key=lambda e: e["mention_count"], reverse=True
    )
    for e in sorted_entities[:15]:
        print(f"  {e['type']:12s} {e['name']:30s} mentions={e['mention_count']:4d} files={len(e['referenced_in'])}")


if __name__ == "__main__":
    main()
