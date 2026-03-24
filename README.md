# book-to-vault-lite

Minimal V1 for turning a technical PDF into chat-ready chapter files, plus the prompts used later to turn study chats into long-term notes.

This repo does only two things:

1. Prepare chapter files from a PDF with `prepare_sections.py`
2. Store the prompts you will later use with ChatGPT, Claude, and Codex

It does not call an LLM automatically.
It does not write into `knowledge-vault`.
It does not add workflow automation.

## Prompt Templates

These prompts are meant for a simple chapter-wise workflow.

### Files

- `prompts/study_prompt.md`  
  Use in ChatGPT or Claude when you paste:
  1. the current per-book global working memory
  2. one chapter markdown file

- `prompts/export_prompt.md`  
  Use at the end of the study chat to generate the final chapter export.

- `prompts/vault_update_prompt.md`  
  Use in Codex after you save the export file locally. This updates the target vault repo.

### What you need to change

Replace placeholders like these before use:

- `<BOOK_TITLE>`
- `<BOOK_AUTHOR>`
- `<BOOK_SLUG>`
- `<CHAPTER_NUMBER>`
- `<CHAPTER_TITLE>`
- `<CHAPTER_FILE_PATH>`
- `<EXPORT_FILE_PATH>`
- `<TARGET_VAULT_REPO>`
- `<BOOK_FOLDER_PATH>`
- `<GLOBAL_MEMORY_PATH>`
- `<BOOK_INDEX_PATH>`
- `<CHAPTER_NOTE_PATH>`

### Recommended flow

1. Run your PDF parsing script and get chapter markdown files.
2. Open one chapter file.
3. In ChatGPT/Claude, paste:
   - the per-book global working memory
   - the chapter markdown
   - `study_prompt.md`
4. Ask questions until you understand the chapter.
5. Paste `export_prompt.md`.
6. Save the result as a markdown export file.
7. Open Codex and paste `vault_update_prompt.md`.
8. Let Codex update the notes in your vault repo.

### Notes

- Global working memory is per book.
- Keep the working memory compact.
- Keep the chapter export detailed.
- The export file is the bridge between the study chat and the vault.

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
