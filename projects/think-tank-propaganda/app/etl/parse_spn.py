#!/usr/bin/env python3
"""
Parse a saved SourceWatch SPN Members HTML page and extract two tables:
  - Affiliate Members
  - Associate Members

Outputs two CSV files in the current working directory by default.

Dependencies:
  pip install beautifulsoup4 lxml pandas
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://www.sourcewatch.org"


def _absolute_url(href: str) -> str:
    if not href:
        return ""
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return BASE_URL + "/" + href


def _read_html(path_str: str) -> str:
    path = Path(path_str)
    if not path.is_file():
        raise FileNotFoundError(f"HTML file not found: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def _clean_lines(tag) -> List[str]:
    for sup in tag.find_all("sup"):
        sup.decompose()
    text = tag.get_text("\n", strip=True)
    return [line.strip() for line in text.split("\n") if line.strip()]


def _extract_as_of(section_header) -> str:
    p = section_header.find_next("p")
    if not p:
        return ""
    lines = _clean_lines(p)
    text = " ".join(lines)
    match = re.search(r"as of ([A-Za-z]+ \d{4})", text)
    return match.group(1) if match else ""


def _find_section_header(soup: BeautifulSoup, label: str):
    headline = soup.find(
        "span",
        class_="mw-headline",
        string=lambda s: s and label in s,
    )
    if not headline:
        raise RuntimeError(f"Could not locate '{label}' headline")
    section_header = headline.find_parent(["h2", "h3"])
    if not section_header:
        raise RuntimeError(f"Could not find parent heading for '{label}'")
    return section_header


def parse_affiliates(soup: BeautifulSoup, source_page: str) -> pd.DataFrame:
    section = _find_section_header(soup, "Affiliate Members")
    as_of = _extract_as_of(section)

    rows: List[Dict[str, str]] = []
    for sib in section.find_all_next():
        if sib == section:
            continue
        if sib.name in ("h2", "h3"):
            break
        if sib.name != "p":
            continue

        lines = _clean_lines(sib)
        if not lines:
            continue
        if lines[0].startswith('"Affiliate Members" include'):
            continue
        if len(lines) < 2:
            continue

        state = lines[0]
        org_line = lines[1]

        a_tags = [a for a in sib.find_all("a", href=True) if not a.find_parent("sup")]
        org_anchor = None
        website_links: List[str] = []
        for a in a_tags:
            href = a.get("href", "")
            if href.startswith("http://") or href.startswith("https://"):
                website_links.append(href)
            elif org_anchor is None:
                org_anchor = a

        org_name = org_anchor.get_text(strip=True) if org_anchor else org_line
        org_sourcewatch_url = _absolute_url(org_anchor.get("href", "")) if org_anchor else ""
        org_sourcewatch_title = org_anchor.get("title", "") if org_anchor else ""
        website = "; ".join(dict.fromkeys(website_links))

        phone = ""
        for line in reversed(lines):
            if line in (state, org_line):
                continue
            if line.startswith("http://") or line.startswith("https://"):
                continue
            if re.search(r"\d", line):
                phone = line
                break

        notes: List[str] = []
        for line in lines:
            if line in (state, org_line):
                continue
            if line.startswith("http://") or line.startswith("https://"):
                continue
            if phone and line == phone:
                continue
            notes.append(line)

        rows.append(
            {
                "member_category": "affiliate",
                "state": state,
                "org_name": org_name,
                "org_name_raw": org_line,
                "notes": " | ".join(notes),
                "website": website,
                "phone": phone,
                "sourcewatch_page_url": org_sourcewatch_url,
                "sourcewatch_page_title": org_sourcewatch_title,
                "as_of": as_of,
                "source_page": source_page,
                "raw_text": " | ".join(lines),
            }
        )

    return pd.DataFrame(rows)


def parse_associates(soup: BeautifulSoup, source_page: str) -> pd.DataFrame:
    section = _find_section_header(soup, "Associate Members")
    as_of = _extract_as_of(section)

    rows: List[Dict[str, str]] = []
    for sib in section.find_all_next():
        if sib == section:
            continue
        if sib.name in ("h2", "h3"):
            break
        if sib.name != "ul":
            continue

        for li in sib.find_all("li", recursive=False):
            for sup in li.find_all("sup"):
                sup.decompose()
            org_name = li.get_text(" ", strip=True)
            a = li.find("a", href=True)
            href = a.get("href", "") if a else ""
            title = a.get("title", "") if a else ""
            classes = set(a.get("class", [])) if a else set()
            is_redlink = "redlink=1" in href or "new" in classes

            rows.append(
                {
                    "member_category": "associate",
                    "org_name": org_name,
                    "sourcewatch_page_url": _absolute_url(href) if href else "",
                    "sourcewatch_page_title": title,
                    "sourcewatch_redlink": str(bool(is_redlink)),
                    "as_of": as_of,
                    "source_page": source_page,
                    "raw_text": org_name,
                }
            )

    return pd.DataFrame(rows)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse a saved SourceWatch SPN Members HTML page",
    )
    parser.add_argument(
        "html_path",
        help="Path to the saved SPN Members HTML file",
    )
    parser.add_argument(
        "--affiliate-out",
        default="spn_affiliate_members.csv",
        help="Output CSV for affiliate members",
    )
    parser.add_argument(
        "--associate-out",
        default="spn_associate_members.csv",
        help="Output CSV for associate members",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    html = _read_html(args.html_path)
    soup = BeautifulSoup(html, "lxml")

    affiliates = parse_affiliates(soup, args.html_path)
    associates = parse_associates(soup, args.html_path)

    affiliates.to_csv(args.affiliate_out, index=False)
    associates.to_csv(args.associate_out, index=False)

    print(f"[SPN] Affiliate members: {len(affiliates)} -> {args.affiliate_out}")
    print(f"[SPN] Associate members: {len(associates)} -> {args.associate_out}")


if __name__ == "__main__":
    main()
