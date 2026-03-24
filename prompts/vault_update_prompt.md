A completed chapter export is now available.

## Context

- Book: <BOOK_TITLE>
- Author: <BOOK_AUTHOR>
- Book slug: <BOOK_SLUG>
- Chapter number: <CHAPTER_NUMBER>
- Chapter title: <CHAPTER_TITLE>

## Read these inputs

- New chapter export: `<EXPORT_FILE_PATH>`
- Existing per-book global working memory if present: `<GLOBAL_MEMORY_PATH>`
- Existing book index if present: `<BOOK_INDEX_PATH>`
- Existing chapter note if present: `<CHAPTER_NOTE_PATH>`

## Target vault repo

`<TARGET_VAULT_REPO>`

## Allowed target paths only

- `<BOOK_FOLDER_PATH>/_system/global_working_memory.md`
- `<BOOK_FOLDER_PATH>/_system/book_index.md`
- `<BOOK_FOLDER_PATH>/chapter<CHAPTER_NUMBER_PADDED>.md`

Do not write outside these paths.

## Tasks

### 1. Update the chapter note
Write or update:

`<BOOK_FOLDER_PATH>/chapter<CHAPTER_NUMBER_PADDED>.md`

Rules:
- Treat the new export as the source of truth for this chapter.
- Preserve as much useful detail as possible.
- Remove repetition, not substance.
- Keep the note readable and well structured.

### 2. Update the per-book global working memory
Write or update:

`<BOOK_FOLDER_PATH>/_system/global_working_memory.md`

Rules:
- This file is per book, not repo-wide.
- Keep it compact and high-signal.
- Preserve only what future chapter chats and future note updates need for continuity.
- Keep stable terminology, core mental models, tricky distinctions, open loops, and progress state.
- Do not turn it into a long chapter summary.

### 3. Update the book index
Write or update:

`<BOOK_FOLDER_PATH>/_system/book_index.md`

Rules:
- Record that this chapter is now completed or updated.
- Keep the progress readable.
- Link to the chapter note.

## Quality rules

- Prefer completeness in the chapter note.
- Prefer compactness in the global working memory.
- Keep the book index short and functional.
- Preserve important distinctions and caveats.
- Avoid unnecessary rewriting if existing content is already good.
- Show exactly which files were changed.