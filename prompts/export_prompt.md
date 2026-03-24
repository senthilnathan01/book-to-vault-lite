EXPORT_CHAPTER_NOTE

Generate a final markdown note for long-term knowledge storage.

This note will be saved in my Obsidian vault and used later for study, revision, cross-linking, and retrieval.

## Context

- Book: <BOOK_TITLE>
- Author: <BOOK_AUTHOR>
- Chapter number: <CHAPTER_NUMBER>
- Chapter title: <CHAPTER_TITLE>

## Primary goal

Preserve as much useful knowledge as possible from:
1. the original chapter text
2. the entire discussion in this chat

## Instructions

- Write a self-contained markdown note.
- Preserve important detail.
- Do not over-compress.
- Keep important nuances, assumptions, tradeoffs, corrections, caveats, counterexamples, and edge cases.
- Preserve examples that materially improved understanding.
- Include clarifications that emerged during the discussion.
- If the discussion corrected an earlier misunderstanding, preserve the corrected understanding.
- Keep terminology precise.
- When useful mental models or reformulations appeared in the chat, preserve them.
- If something remains uncertain, mark it clearly instead of smoothing it over.
- Make the note useful months later without needing the original chat.
- Output only markdown. Do not use code fences.
- If needed, continue in multiple parts rather than omitting important material.

## Required structure

# <Chapter Note Title>

## Source
- Book: <BOOK_TITLE>
- Author: <BOOK_AUTHOR>
- Chapter: <CHAPTER_NUMBER> — <CHAPTER_TITLE>
- Source file: <CHAPTER_FILE_PATH>

## Chapter Thesis
A short paragraph explaining the main point of this chapter.

## Chapter Structure
- Major subsection/grouping -> role in the chapter

## Detailed Notes
Write the detailed explanation here.

## Key Ideas And Mechanisms
- ...

## Important Examples
- ...

## Caveats And Edge Cases
- ...

## Clarifications From Discussion
- Include corrections, refinements, distinctions, and useful reformulations from the chat.

## Terms And Definitions
- Term: definition

## Connections
- Link this chapter to earlier or later parts of the book when relevant.
- Mention reusable concept-note candidates if appropriate.

## Open Questions
- Only include real unresolved points.

## Practical Takeaways
- ...

## Final instruction

Before writing, internally review the entire conversation and preserve every nontrivial technical insight that emerged during the discussion.