#!/usr/bin/env python3
"""Fetch a small, permitted set of public pages into Markdown files.

This optional helper is deliberately conservative: it checks robots.txt, waits
between requests, and accepts only HTML/text pages. It is not a site crawler.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser


DEFAULT_USER_AGENT = "Day7DataFoundationsCourse/1.0 (+educational-lab)"
MANIFEST_FIELDS = ["doc_id", "file_path", "title", "source_url", "retrieved_at", "document_version", "license_or_permission"]
BLOCK_TAGS = {"p", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "div", "section", "article"}
SKIP_TAGS = {"script", "style", "nav", "footer", "header", "noscript", "svg", "iframe"}
SAFE_METADATA_KEY = re.compile(r"^[a-z][a-z0-9_]*$")


class TextExtractor(HTMLParser):
    """A dependency-free HTML-to-text extractor for simple public pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.in_title = False
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = True
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = False
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            if self.in_title:
                self.title_parts.append(data)
            self.parts.append(data)

    def text(self) -> str:
        text = re.sub(r"[ \t]+", " ", "".join(self.parts))
        text = re.sub(r"\n[ \t]+", "\n", text)
        return re.sub(r"\n{3,}", "\n\n", text).strip()

    def page_title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower().strip())
    return value.strip("-") or "document"


def yaml_value(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as source_file:
        reader = csv.DictReader(source_file)
        if not reader.fieldnames or "url" not in reader.fieldnames:
            raise ValueError("Input CSV must have a 'url' column.")
        rows = []
        for number, row in enumerate(reader, start=2):
            cleaned = {key.strip(): (value or "").strip() for key, value in row.items() if key}
            if not cleaned.get("url"):
                print(f"Skipping row {number}: missing url", file=sys.stderr)
            else:
                rows.append(cleaned)
    return rows


def robots_allowed(url: str, user_agent: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        print(f"Skipping unsupported URL: {url}", file=sys.stderr)
        return False
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = RobotFileParser(robots_url)
    try:
        parser.read()
    except (HTTPError, URLError, OSError) as error:
        print(f"Skipping {url}: cannot verify {robots_url} ({error})", file=sys.stderr)
        return False
    if not parser.can_fetch(user_agent, url):
        print(f"Skipping {url}: disallowed by robots.txt", file=sys.stderr)
        return False
    return True


def fetch(url: str, user_agent: str, timeout: float) -> tuple[str, str]:
    request = Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,text/plain;q=0.9,*/*;q=0.1"})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - URL is supplied by the course user.
        content_type = response.headers.get_content_type().lower()
        if content_type not in {"text/html", "text/plain"}:
            raise ValueError(f"unsupported content type: {content_type}")
        charset = response.headers.get_content_charset() or "utf-8"
        return response.geturl(), response.read().decode(charset, errors="replace")


def extract_content(body: str) -> tuple[str, str]:
    parser = TextExtractor()
    parser.feed(body)
    parser.close()
    return parser.page_title(), parser.text()


def existing_manifest(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as manifest_file:
        return {row["doc_id"]: row for row in csv.DictReader(manifest_file) if row.get("doc_id")}


def write_manifest(path: Path, records: dict[str, dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as manifest_file:
        writer = csv.DictWriter(manifest_file, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for doc_id in sorted(records):
            writer.writerow({field: records[doc_id].get(field, "") for field in MANIFEST_FIELDS})


def markdown_document(metadata: dict[str, str], content: str) -> str:
    front_matter = "\n".join(f"{key}: {yaml_value(value)}" for key, value in metadata.items())
    return f"---\n{front_matter}\n---\n\n# {metadata['title']}\n\n{content}\n"


def build_metadata(row: dict[str, str], final_url: str, title: str) -> dict[str, str]:
    document_id = slugify(row.get("doc_id") or Path(urlparse(final_url).path).stem or title)
    metadata = {
        "doc_id": document_id,
        "title": row.get("title") or title or document_id.replace("-", " ").title(),
        "source_url": final_url,
        "retrieved_at": date.today().isoformat(),
        "document_version": row.get("document_version") or "not-stated",
    }
    excluded = {"url", "doc_id", "title", "document_version"}
    metadata.update({key: value for key, value in row.items() if key not in excluded and value and SAFE_METADATA_KEY.match(key)})
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch a small list of allowed public pages into Markdown.")
    parser.add_argument("input_csv", type=Path, help="CSV with a required 'url' column")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for .md files and sources.csv")
    parser.add_argument("--delay", type=float, default=1.0, help="Minimum seconds between requests (default: 1.0)")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds (default: 20)")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing Markdown file with the same doc_id")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.delay < 1:
        print("--delay must be at least 1 second to respect source websites.", file=sys.stderr)
        return 2
    if not args.input_csv.is_file():
        print(f"Input file not found: {args.input_csv}", file=sys.stderr)
        return 2
    try:
        rows = load_rows(args.input_csv)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output_dir / "sources.csv"
    manifest = existing_manifest(manifest_path)
    successful = failed = 0
    for index, row in enumerate(rows):
        url = row["url"]
        if not robots_allowed(url, args.user_agent):
            failed += 1
            continue
        if index:
            time.sleep(args.delay)
        try:
            final_url, body = fetch(url, args.user_agent, args.timeout)
            title, content = extract_content(body)
            if len(content) < 80:
                raise ValueError("extracted content is too short; use another source or clean it manually")
            metadata = build_metadata(row, final_url, title)
            output_path = args.output_dir / f"{metadata['doc_id']}.md"
            if output_path.exists() and not args.overwrite:
                raise FileExistsError(f"{output_path} exists (use --overwrite to replace it)")
            output_path.write_text(markdown_document(metadata, content), encoding="utf-8")
            manifest[metadata["doc_id"]] = {
                "doc_id": metadata["doc_id"], "file_path": str(output_path).replace("\\", "/"), "title": metadata["title"],
                "source_url": metadata["source_url"], "retrieved_at": metadata["retrieved_at"],
                "document_version": metadata["document_version"],
                "license_or_permission": row.get("license_or_permission") or "public-source",
            }
            successful += 1
            print(f"Saved {output_path}")
        except (HTTPError, URLError, TimeoutError, UnicodeError, LookupError, ValueError, OSError) as error:
            failed += 1
            print(f"Skipping {url}: {error}", file=sys.stderr)
    write_manifest(manifest_path, manifest)
    print(f"Finished: {successful} saved, {failed} skipped. Manifest: {manifest_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

