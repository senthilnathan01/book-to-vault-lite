# book-to-vault-lite

Minimal V1 for turning a technical PDF into chat-ready chapter files, plus the prompts used later to turn study chats into long-term notes.

This repo does only two things:

1. Prepare chapter files from a PDF with `prepare_sections.py`
2. Store the prompts you will later use with ChatGPT, Claude, and Codex

It does not call an LLM automatically.
It does not write into `knowledge-vault`.
It does not add workflow automation.

## Minimal workflow

1. Put a technical PDF somewhere local.
2. Run `prepare_sections.py` against that PDF.
3. Copy one generated chapter file at a time into ChatGPT or Claude.
4. Study the chapter and export the final detailed markdown manually.
5. Later, use Codex with the prompts in [`prompts/final_export_prompt.md`](/Users/tsn/Documents/book-to-vault-lite/prompts/final_export_prompt.md), [`prompts/chapter_summary_prompt.md`](/Users/tsn/Documents/book-to-vault-lite/prompts/chapter_summary_prompt.md), and [`prompts/global_summary_prompt.md`](/Users/tsn/Documents/book-to-vault-lite/prompts/global_summary_prompt.md) to update notes in the separate `knowledge-vault` repo.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python prepare_sections.py \
  --pdf /path/to/technical_book.pdf \
  --book-slug technical_book_slug \
  --book-title "Technical Book Title" \
  --author "Author Name"
```

Supported arguments:

- `--pdf`: required PDF path
- `--book-slug`: output folder name under `data/processed/`
- `--book-title`: metadata title override
- `--author`: optional metadata
- `--output-dir`: optional base output directory, default `data/processed`

## What the script does

- extracts text page by page from the PDF
- strips repeated headers, footers, and simple page numbers where it can
- tries to split on chapter headings such as `Chapter 1` and isolated top-level headings like `1 Introduction`
- uses section-style headings such as `1.1`, `1.2.3`, all-caps headings, and isolated title-style headings as internal subheadings inside each chapter file when useful
- falls back to chapter-sized page-window chunking when chapter detection is weak
- writes one markdown file per chapter under `data/processed/<book_slug>/`

Example output layout:

```text
data/processed/<book_slug>/
  chapter01.md
  chapter02.md
  chapter03.md
```

Each generated file starts with metadata:

- Book
- Author
- Chapter
- Source pages
- Chunk id

The chapter files are formatted so they can be pasted directly into a chapter study chat.

## Prompts

- [`prompts/final_export_prompt.md`](/Users/tsn/Documents/book-to-vault-lite/prompts/final_export_prompt.md): use at the end of a chapter study chat to produce a detailed long-term markdown export
- [`prompts/chapter_summary_prompt.md`](/Users/tsn/Documents/book-to-vault-lite/prompts/chapter_summary_prompt.md): use later with Codex to turn a detailed chapter export into a readable chapter summary
- [`prompts/global_summary_prompt.md`](/Users/tsn/Documents/book-to-vault-lite/prompts/global_summary_prompt.md): use later with Codex to maintain a compact per-book working memory file

## Vault assumptions

This repo assumes `knowledge-vault` is a separate repo.

The prompts assume a target structure like:

```text
01_books/<book_slug>/_system/global_working_memory.md
01_books/<book_slug>/_system/book_index.md
01_books/<book_slug>/chapter_01/chapter_note.md
01_books/<book_slug>/chapter_01/chapter_summary.md
02_concepts/
```

Important: global working memory is per book and belongs under the book folder, for example:

```text
01_books/<book_slug>/_system/global_working_memory.md
```

It should not live in a repo-wide system folder.

## Notes on quality

This is intentionally a small V1. It is designed to work for a normal text-based technical PDF, not every possible PDF layout.

If extraction quality is poor, the script warns clearly. If heading detection is weak, it falls back to chapter-sized page-window chunking and tells you that explicitly.
