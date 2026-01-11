#!/usr/bin/env python3
"""
Convert a CSV file to JSON.

Example:
  python csv_to_json.py \
    --in final.csv \
    --out final.json
"""

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_IN_PATH = "final.csv"
DEFAULT_OUT_PATH = "final.json"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert CSV to JSON")
    parser.add_argument(
        "--in",
        dest="in_path",
        default=DEFAULT_IN_PATH,
        help="Path to input CSV",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        default=DEFAULT_OUT_PATH,
        help="Path to output JSON",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (0 for compact)",
    )
    return parser.parse_args()


def _is_empty(value: str) -> bool:
    if value is None:
        return True
    cleaned = str(value).strip()
    if not cleaned:
        return True
    return cleaned.lower() in {"-", "—", "na", "n/a", "none", "null"}


def _normalize_text(value: str) -> str:
    if _is_empty(value):
        return ""
    cleaned = str(value).strip().lower()
    cleaned = re.sub(r"[\.,;:]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _normalize_location(value: str) -> str:
    cleaned = _normalize_text(value)
    if not cleaned:
        return ""
    cleaned = re.sub(r"\b(u\.s\.a\.|u\.s\.|us)\b", "usa", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _normalize_website(value: str) -> str:
    if _is_empty(value):
        return ""
    cleaned = str(value).strip().lower()
    cleaned = re.sub(r"^https?://", "", cleaned)
    cleaned = re.sub(r"^www\.", "", cleaned)
    cleaned = cleaned.rstrip("/")
    return cleaned


def _get_field(row: Dict[str, str], names: Tuple[str, ...]) -> str:
    for name in names:
        if name in row and not _is_empty(row.get(name)):
            return str(row.get(name))
    return ""


def _row_key(row: Dict[str, str]) -> str:
    org = _normalize_text(_get_field(row, ("org_name", "Organization", "organization", "institution")))
    loc = _normalize_location(_get_field(row, ("location", "Location")))
    site = _normalize_website(_get_field(row, ("website", "Website", "url", "URL")))

    if org and loc:
        return f"org:{org}|loc:{loc}"
    if org and site:
        return f"org:{org}|site:{site}"
    if org:
        return f"org:{org}"
    if site:
        return f"site:{site}"
    if loc:
        return f"loc:{loc}"
    return "unknown"


def _location_tokens(value: str) -> Tuple[str, ...]:
    cleaned = _normalize_location(value)
    if not cleaned:
        return tuple()
    tokens = re.findall(r"[a-z0-9]+", cleaned)
    return tuple(sorted(set(tokens)))


def _location_similarity(a: Tuple[str, ...], b: Tuple[str, ...]) -> float:
    if not a or not b:
        return 0.0
    set_a = set(a)
    set_b = set(b)
    shared = len(set_a & set_b)
    min_size = min(len(set_a), len(set_b))
    if min_size == 0:
        return 0.0
    return shared / min_size


def _merge_rows(base: Dict[str, str], other: Dict[str, str]) -> Dict[str, str]:
    merged = dict(base)
    for key, value in other.items():
        if _is_empty(merged.get(key)) and not _is_empty(value):
            merged[key] = value
    return merged


def _row_score(row: Dict[str, str]) -> int:
    return sum(1 for value in row.values() if not _is_empty(value))


def _dedupe_rows(rows: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], int]:
    groups: Dict[str, List[Dict[str, object]]] = {}
    deduped: List[Dict[str, str]] = []
    duplicates = 0

    for row in rows:
        org = _normalize_text(_get_field(row, ("org_name", "Organization", "organization", "institution")))
        loc_tokens = _location_tokens(_get_field(row, ("location", "Location")))
        site = _normalize_website(_get_field(row, ("website", "Website", "url", "URL")))
        score = _row_score(row)

        if not org:
            key = _row_key(row)
            if key == "unknown":
                deduped.append(row)
                continue
            groups.setdefault(key, []).append(
                {"row": row, "loc_tokens": loc_tokens, "site": site, "score": score}
            )
            continue

        candidates = groups.setdefault(f"org:{org}", [])
        matched = False
        for entry in candidates:
            entry_site = entry["site"]
            if site and entry_site and site == entry_site:
                merged = _merge_rows(entry["row"], row)
                merged_score = _row_score(merged)
                if merged_score >= entry["score"]:
                    entry["row"] = merged
                    entry["score"] = merged_score
                    entry["loc_tokens"] = _location_tokens(
                        _get_field(merged, ("location", "Location"))
                    )
                    entry["site"] = _normalize_website(_get_field(merged, ("website", "Website", "url", "URL")))
                duplicates += 1
                matched = True
                break

            similarity = _location_similarity(loc_tokens, entry["loc_tokens"])
            if similarity >= 0.9:
                merged = _merge_rows(entry["row"], row)
                merged_score = _row_score(merged)
                if merged_score >= entry["score"]:
                    entry["row"] = merged
                    entry["score"] = merged_score
                    entry["loc_tokens"] = _location_tokens(
                        _get_field(merged, ("location", "Location"))
                    )
                    entry["site"] = _normalize_website(_get_field(merged, ("website", "Website", "url", "URL")))
                duplicates += 1
                matched = True
                break

        if not matched:
            candidates.append(
                {"row": row, "loc_tokens": loc_tokens, "site": site, "score": score}
            )

    for key, entries in groups.items():
        for entry in entries:
            deduped.append(entry["row"])

    return deduped, duplicates


def main() -> None:
    args = _parse_args()
    in_path = Path(args.in_path)
    out_path = Path(args.out_path)

    with in_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    deduped_rows, duplicates = _dedupe_rows(rows)
    indent = None if args.indent == 0 else args.indent
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(deduped_rows, f, ensure_ascii=True, indent=indent)

    print(f"Wrote {len(deduped_rows)} rows to {out_path} (removed {duplicates} duplicates)")


if __name__ == "__main__":
    main()
