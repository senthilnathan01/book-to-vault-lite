# Global Summary Prompt

Use this later with Codex to create or update the per-book global working memory file.

Target location example:

`01_books/<book_slug>/_system/global_working_memory.md`

This file is per book. It is not a repo-wide system note.

## Inputs

- the existing per-book `global_working_memory.md` if present
- recent section notes and chapter summaries
- any current study progress information that matters for continuity

## Instructions

- Produce a compact markdown working-memory file for this single book.
- Keep only high-signal continuity information that will help future study chats or note-updating work.
- Do not turn this into a long chapter note or a full book summary.
- Preserve stable terminology, key mental models, important unresolved questions, recurring confusions, and progress state.
- Keep it compact enough to paste into future chats.
- Prefer durable information over temporary detail.
- If an existing working-memory file already has good structure, update it incrementally instead of rewriting needlessly.
- Output only markdown. Do not use code fences.

## Suggested structure

```markdown
# Global Working Memory

## Book
- Title:
- Author:
- Vault path:

## Current Progress
- Last completed chapter/section:
- What is currently in progress:

## Core Mental Models
- ...

## Stable Terminology
- Term: short meaning in the context of this book

## Important Cross-Chapter Threads
- ...

## Recurring Confusions Or Tricky Distinctions
- ...

## Open Loops
- Unresolved questions worth carrying forward

## Concept Note Candidates
- Potential reusable notes for `02_concepts/`
```

## Quality bar

- Keep it compact and high signal.
- Optimize for future continuity, not completeness.
- If something is already obvious from chapter notes, do not repeat it unless it is important for future chats.
