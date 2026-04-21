#!/usr/bin/env python3
"""Sync publication front matter dates from venue timing metadata.

This script uses `_data/publication_venues.json` as the source of truth for
venue timing. For any `_publications/*.md` file whose front matter contains a
recognized `venue`, it rewrites the `date` field so that sorting by `date`
matches the venue's usual place in the calendar.

The day values in the JSON file are synthetic sort keys. They are not intended
to be exact conference dates; they simply keep venues in a stable within-year
order and ensure papers from the same venue sort together.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PUBLICATIONS_DIR = ROOT / "_publications"
VENUE_FILE = ROOT / "_data" / "publication_venues.json"


FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
FIELD_RE = re.compile(r"^(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)$")


def normalize_venue(raw_value: str) -> str:
    value = raw_value.strip().strip("'\"")
    value = re.sub(r"\b20\d{2}\b", "", value.upper())
    value = re.sub(r"[^A-Z]+", " ", value).strip()
    return value


def extract_year(front_matter_lines: list[str]) -> str | None:
    for line in front_matter_lines:
        match = FIELD_RE.match(line)
        if not match:
            continue
        if match.group("key") == "year":
            value = match.group("value").strip().strip("'\"")
            if re.fullmatch(r"\d{4}", value):
                return value

    for line in front_matter_lines:
        match = FIELD_RE.match(line)
        if not match:
            continue
        if match.group("key") == "date":
            value = match.group("value").strip().strip("'\"")
            date_match = re.match(r"(\d{4})-\d{2}-\d{2}", value)
            if date_match:
                return date_match.group(1)

    return None


def sync_file(path: Path, venue_schedule: dict[str, dict[str, int]]) -> bool:
    original = path.read_text(encoding="utf-8")
    front_matter_match = FRONT_MATTER_RE.match(original)
    if not front_matter_match:
        return False

    front_matter = front_matter_match.group(1)
    lines = front_matter.splitlines()

    venue_value = None
    date_index = None

    for index, line in enumerate(lines):
        match = FIELD_RE.match(line)
        if not match:
            continue
        key = match.group("key")
        value = match.group("value")
        if key == "venue":
            venue_value = value
        elif key == "date":
            date_index = index

    if venue_value is None:
        return False

    venue_key = normalize_venue(venue_value)
    if venue_key not in venue_schedule:
        return False

    year = extract_year(lines)
    if year is None:
        return False

    month = venue_schedule[venue_key]["month"]
    day = venue_schedule[venue_key]["day"]
    new_date = f"{year}-{month:02d}-{day:02d}"

    if date_index is not None:
        if lines[date_index] == f"date: {new_date}":
            return False
        lines[date_index] = f"date: {new_date}"
    else:
        insert_at = 0
        for index, line in enumerate(lines):
            if line.startswith("permalink:"):
                insert_at = index + 1
                break
        lines.insert(insert_at, f"date: {new_date}")

    new_front_matter = "\n".join(lines)
    updated = original[: front_matter_match.start(1)] + new_front_matter + original[front_matter_match.end(1) :]
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    venue_schedule = json.loads(VENUE_FILE.read_text(encoding="utf-8"))
    updated_files = []

    for path in sorted(PUBLICATIONS_DIR.glob("*.md")):
        if sync_file(path, venue_schedule):
            updated_files.append(path.name)

    if updated_files:
        print("Updated publication dates:")
        for name in updated_files:
            print(f" - {name}")
    else:
        print("No publication dates needed updating.")


if __name__ == "__main__":
    main()
