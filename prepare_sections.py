#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


CHAPTER_RE = re.compile(r"^(chapter|chap\.)\s+(\d+|[ivxlcdm]+)\b[\s:.-]*(.*)$", re.IGNORECASE)
SECTION_RE = re.compile(r"^(\d+(?:\.\d+){1,3})\s+(.+)$")
PAGE_NUMBER_RE = re.compile(r"^(?:page\s+)?\d+$", re.IGNORECASE)
SIMPLE_HEADING_RE = re.compile(r"^(\d+)\s+([A-Z][^.?!]{1,90})$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a technical PDF into chat-ready markdown section files."
    )
    parser.add_argument("--pdf", required=True, help="Path to the source PDF.")
    parser.add_argument("--book-slug", help="Stable slug used for the output folder.")
    parser.add_argument("--book-title", help="Book title for metadata.")
    parser.add_argument("--author", help="Optional author name for metadata.")
    parser.add_argument(
        "--output-dir",
        default="data/processed",
        help="Base output directory inside this repo. Default: data/processed",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "book"


def roman_to_int(token: str) -> int | None:
    values = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
    token = token.lower()
    if not token or any(char not in values for char in token):
        return None

    total = 0
    previous = 0
    for char in reversed(token):
        value = values[char]
        if value < previous:
            total -= value
        else:
            total += value
            previous = value
    return total


def parse_numeric_token(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    return roman_to_int(token)


def normalize_repeat_key(line: str) -> str:
    line = re.sub(r"\s+", " ", line.strip().lower())
    line = re.sub(r"\b\d+\b", "<n>", line)
    if not line or len(line) > 100:
        return ""
    return line


def is_probable_page_number(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return bool(PAGE_NUMBER_RE.fullmatch(stripped))


def extract_pages(pdf_path: Path) -> tuple[list[dict], list[str]]:
    try:
        import fitz
    except ImportError:
        print(
            "Missing dependency: PyMuPDF is required. Install with `pip install -r requirements.txt`.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    warnings: list[str] = []
    pages: list[dict] = []

    try:
        document = fitz.open(pdf_path)
    except Exception as exc:  # pragma: no cover - library/runtime dependent
        print(f"Failed to open PDF: {exc}", file=sys.stderr)
        raise SystemExit(1)

    with document:
        for page_index, page in enumerate(document, start=1):
            raw_text = page.get_text("text")
            lines = [line.rstrip() for line in raw_text.splitlines()]
            alpha_chars = sum(1 for char in raw_text if char.isalpha())
            pages.append(
                {
                    "page_num": page_index,
                    "lines": lines,
                    "alpha_chars": alpha_chars,
                }
            )

    if not pages:
        print("The PDF did not contain any readable pages.", file=sys.stderr)
        raise SystemExit(1)

    average_alpha = sum(page["alpha_chars"] for page in pages) / max(len(pages), 1)
    if average_alpha < 350:
        warnings.append(
            "Extraction quality looks low (few readable characters per page). "
            "This may be a scanned PDF or a layout PyMuPDF cannot recover cleanly."
        )

    return pages, warnings


def strip_repeated_margins(pages: list[dict]) -> None:
    top_counts: Counter[str] = Counter()
    bottom_counts: Counter[str] = Counter()

    for page in pages:
        non_empty = [line.strip() for line in page["lines"] if line.strip()]
        for line in non_empty[:2]:
            key = normalize_repeat_key(line)
            if key:
                top_counts[key] += 1
        for line in non_empty[-2:]:
            key = normalize_repeat_key(line)
            if key:
                bottom_counts[key] += 1

    threshold = max(3, int(len(pages) * 0.4))
    repeated_top = {key for key, count in top_counts.items() if count >= threshold}
    repeated_bottom = {key for key, count in bottom_counts.items() if count >= threshold}

    for page in pages:
        lines = list(page["lines"])
        non_empty_indexes = [idx for idx, line in enumerate(lines) if line.strip()]

        for idx in non_empty_indexes[:2]:
            if normalize_repeat_key(lines[idx]) in repeated_top:
                lines[idx] = ""
        for idx in non_empty_indexes[-2:]:
            if normalize_repeat_key(lines[idx]) in repeated_bottom:
                lines[idx] = ""

        page["lines"] = [line for line in lines if not is_probable_page_number(line)]


def looks_like_title_case_heading(text: str) -> bool:
    words = text.split()
    if not (2 <= len(words) <= 12):
        return False
    if text.endswith((".", "?", "!", ";", ",")):
        return False
    capitalized = sum(1 for word in words if word[:1].isupper())
    lower_words = {
        "a",
        "an",
        "and",
        "as",
        "at",
        "by",
        "for",
        "from",
        "in",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
    acceptable = sum(
        1 for word in words if word[:1].isupper() or word.lower() in lower_words
    )
    return capitalized >= 1 and acceptable == len(words)


def parse_heading(text: str, prev_text: str, next_text: str) -> dict | None:
    stripped = text.strip()
    if not stripped or len(stripped) > 100:
        return None

    prev_blank = not prev_text.strip()
    next_blank = not next_text.strip()
    isolated = prev_blank or next_blank

    match = CHAPTER_RE.match(stripped)
    if match:
        number_token = match.group(2)
        explicit_title = match.group(3).strip(" :-.")
        chapter_number = parse_numeric_token(number_token)
        label = f"Chapter {number_token}"
        if explicit_title:
            label = f"{label} - {explicit_title}"
        return {
            "kind": "chapter",
            "chapter_number": chapter_number,
            "label": label,
        }

    match = SECTION_RE.match(stripped)
    if match and isolated:
        number_token = match.group(1)
        return {
            "kind": "section",
            "section_number": number_token,
            "chapter_hint": int(number_token.split(".")[0]),
            "label": stripped,
        }

    match = SIMPLE_HEADING_RE.match(stripped)
    if match and prev_blank and next_blank and len(stripped.split()) <= 10:
        return {
            "kind": "section",
            "section_number": match.group(1),
            "chapter_hint": int(match.group(1)),
            "label": stripped,
        }

    if stripped.isupper() and isolated:
        words = stripped.split()
        if 2 <= len(words) <= 10 and sum(char.isalpha() for char in stripped) >= 6:
            return {"kind": "generic", "label": stripped.title()}

    if prev_blank and next_blank and looks_like_title_case_heading(stripped):
        return {"kind": "generic", "label": stripped}

    return None


def flatten_pages(pages: list[dict]) -> list[dict]:
    records: list[dict] = []
    for page in pages:
        for line in page["lines"]:
            records.append({"page_num": page["page_num"], "text": line})
        records.append({"page_num": page["page_num"], "text": ""})
    return records


def default_chapter(chapter_index: int) -> dict:
    return {
        "index": max(chapter_index, 1),
        "number": None,
        "title": "Unspecified",
    }


def make_chunk(chapter: dict, section_index: int, title: str, start_page: int) -> dict:
    return {
        "chapter_index": chapter["index"],
        "chapter_number": chapter["number"],
        "chapter_title": chapter["title"],
        "section_index": section_index,
        "section_title": title,
        "start_page": start_page,
        "end_page": start_page,
        "lines": [],
    }


def content_char_count(lines: list[str]) -> int:
    return sum(len(line.strip()) for line in lines if line.strip())


def render_markdown(lines: list[str]) -> str:
    blocks: list[str] = []
    paragraph_lines: list[str] = []
    bullet_mode = False

    def flush_paragraph() -> None:
        nonlocal paragraph_lines, bullet_mode
        if not paragraph_lines:
            bullet_mode = False
            return

        if bullet_mode:
            blocks.append("\n".join(paragraph_lines))
        else:
            merged = []
            for line in paragraph_lines:
                if not merged:
                    merged.append(line)
                    continue
                if merged[-1].endswith("-") and line[:1].islower():
                    merged[-1] = merged[-1][:-1] + line
                else:
                    merged[-1] = merged[-1] + " " + line
            blocks.append(merged[-1])

        paragraph_lines = []
        bullet_mode = False

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            continue

        is_bullet = bool(re.match(r"^([-*•]|\d+\.)\s+", line))
        if paragraph_lines and is_bullet != bullet_mode:
            flush_paragraph()

        paragraph_lines.append(line)
        bullet_mode = is_bullet

    flush_paragraph()
    return "\n\n".join(block for block in blocks if block.strip())


def finalize_chunk(chunks: list[dict], chunk: dict | None) -> None:
    if not chunk:
        return
    if content_char_count(chunk["lines"]) < 80:
        return
    chunk["content"] = render_markdown(chunk["lines"])
    if chunk["content"].strip():
        chunks.append(chunk)


def build_heading_chunks(pages: list[dict]) -> tuple[list[dict], dict]:
    records = flatten_pages(pages)
    chunks: list[dict] = []
    current_chunk: dict | None = None
    chapter = default_chapter(1)
    chapter_index = 1
    section_index = 0
    heading_hits = 0
    generic_hits = 0
    explicit_chapters = 0

    for idx, record in enumerate(records):
        text = record["text"]
        prev_text = records[idx - 1]["text"] if idx > 0 else ""
        next_text = records[idx + 1]["text"] if idx + 1 < len(records) else ""
        heading = parse_heading(text, prev_text, next_text)

        if heading and heading["kind"] == "chapter":
            finalize_chunk(chunks, current_chunk)
            heading_hits += 1
            explicit_chapters += 1
            parsed_number = heading.get("chapter_number")
            if parsed_number:
                chapter_index = parsed_number
            elif chunks or current_chunk:
                chapter_index += 1
            chapter = {
                "index": max(chapter_index, 1),
                "number": parsed_number,
                "title": heading["label"],
            }
            section_index = 0
            current_chunk = None
            continue

        if heading and heading["kind"] in {"section", "generic"}:
            if heading["kind"] == "generic":
                generic_hits += 1
            else:
                chapter_hint = heading.get("chapter_hint")
                if chapter["title"] == "Unspecified" and chapter_hint:
                    chapter = {
                        "index": chapter_hint,
                        "number": chapter_hint,
                        "title": f"Chapter {chapter_hint}",
                    }
                    chapter_index = chapter_hint

            if current_chunk and content_char_count(current_chunk["lines"]) < 80:
                current_chunk["section_title"] = heading["label"]
                continue

            finalize_chunk(chunks, current_chunk)
            heading_hits += 1
            section_index += 1
            current_chunk = make_chunk(
                chapter=chapter,
                section_index=section_index,
                title=heading["label"],
                start_page=record["page_num"],
            )
            continue

        if not current_chunk:
            section_index += 1
            title = (
                chapter["title"]
                if chapter["title"] != "Unspecified"
                else f"Opening chunk {section_index}"
            )
            current_chunk = make_chunk(
                chapter=chapter,
                section_index=section_index,
                title=title,
                start_page=record["page_num"],
            )

        current_chunk["lines"].append(text)
        current_chunk["end_page"] = record["page_num"]

    finalize_chunk(chunks, current_chunk)
    stats = {
        "heading_hits": heading_hits,
        "generic_hits": generic_hits,
        "explicit_chapters": explicit_chapters,
    }
    return chunks, stats


def build_fallback_chunks(pages: list[dict]) -> list[dict]:
    chunks: list[dict] = []
    chapter = {"index": 1, "number": None, "title": "Fallback chapter"}
    section_index = 0
    current_chunk: dict | None = None

    for page in pages:
        page_chars = content_char_count(page["lines"])
        if page_chars < 80:
            continue

        if not current_chunk:
            section_index += 1
            current_chunk = make_chunk(
                chapter=chapter,
                section_index=section_index,
                title=f"Fallback chunk {section_index}",
                start_page=page["page_num"],
            )

        projected_pages = page["page_num"] - current_chunk["start_page"] + 1
        projected_chars = content_char_count(current_chunk["lines"]) + page_chars

        if current_chunk["lines"] and (projected_pages > 8 or projected_chars > 18000):
            finalize_chunk(chunks, current_chunk)
            section_index += 1
            current_chunk = make_chunk(
                chapter=chapter,
                section_index=section_index,
                title=f"Fallback chunk {section_index}",
                start_page=page["page_num"],
            )

        current_chunk["lines"].extend(page["lines"])
        current_chunk["lines"].append("")
        current_chunk["end_page"] = page["page_num"]

    finalize_chunk(chunks, current_chunk)
    return chunks


def write_chunks(
    chunks: list[dict],
    output_dir: Path,
    book_title: str,
    author: str,
) -> list[Path]:
    written_files: list[Path] = []

    for chunk in chunks:
        chapter_dir = output_dir / f"chapter_{chunk['chapter_index']:02d}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        output_path = chapter_dir / f"section_{chunk['section_index']:02d}.md"

        chapter_label = chunk["chapter_title"]
        if chunk["chapter_number"] and chapter_label == "Unspecified":
            chapter_label = f"Chapter {chunk['chapter_number']}"

        metadata = [
            "# Section Chunk",
            "",
            f"- Book: {book_title}",
            f"- Author: {author or 'Unknown'}",
            f"- Chapter: {chapter_label}",
            f"- Section: {chunk['section_title']}",
            f"- Source pages: {chunk['start_page']}-{chunk['end_page']}",
            f"- Chunk id: chapter_{chunk['chapter_index']:02d}_section_{chunk['section_index']:02d}",
            "",
            "## Notes",
            "This file is intended to be pasted into a study chat together with the current per-book global working memory.",
            "",
            "## Content",
            chunk["content"].strip(),
            "",
        ]

        output_path.write_text("\n".join(metadata), encoding="utf-8")
        written_files.append(output_path)

    return written_files


def main() -> int:
    args = parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1
    if pdf_path.suffix.lower() != ".pdf":
        print("The input file must be a PDF.", file=sys.stderr)
        return 1

    book_title = args.book_title or pdf_path.stem.replace("_", " ").replace("-", " ").strip()
    book_slug = args.book_slug or slugify(book_title or pdf_path.stem)
    output_root = Path(args.output_dir).expanduser().resolve() / book_slug

    pages, warnings = extract_pages(pdf_path)
    strip_repeated_margins(pages)

    heading_chunks, stats = build_heading_chunks(pages)
    use_heading_split = len(heading_chunks) >= 2 and stats["heading_hits"] >= 2
    split_mode = "heading-based"
    confidence = "good"

    if not use_heading_split:
        chunks = build_fallback_chunks(pages)
        split_mode = "fallback page-window chunking"
        confidence = "limited"
        warnings.append(
            "Heading detection was weak, so the script fell back to page-window chunking."
        )
    else:
        chunks = heading_chunks
        if stats["generic_hits"] > stats["heading_hits"] // 2:
            confidence = "moderate"

    if not chunks:
        print(
            "No usable chunks were produced. The PDF may be image-only or extraction quality may be too low.",
            file=sys.stderr,
        )
        return 1

    written_files = write_chunks(
        chunks=chunks,
        output_dir=output_root,
        book_title=book_title,
        author=args.author or "",
    )

    print(f"Output directory: {output_root}")
    print(f"Chunks written: {len(written_files)}")
    print(f"Split mode: {split_mode}")
    print(f"Split confidence: {confidence}")
    for warning in warnings:
        print(f"Warning: {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
