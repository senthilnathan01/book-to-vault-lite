# Chapter Summary Prompt

Use this later with Codex after you already have a detailed chapter export for a chapter.

Your job is to update or create a readable chapter summary from the detailed chapter export.

This is a synthesis task, not a copy-and-shorten task.

## Inputs

- the current `chapter_summary.md` if it already exists
- the detailed chapter export for the chapter
- optional per-book global working memory if it helps maintain continuity

## Instructions

- Produce a chapter-level markdown summary.
- Synthesize the chapter's overall argument, progression, and important mechanisms.
- Preserve important detail that matters at chapter scope.
- Do not just trim the chapter export down mechanically.
- Keep the writing readable and coherent.
- Merge overlapping ideas.
- Preserve important distinctions, caveats, tradeoffs, and recurring examples.
- If the existing chapter summary already contains good material, keep and improve it instead of rewriting gratuitously.
- Call out where the chapter changes the reader's mental model, introduces a framework, or sets up later chapters.
- Output only markdown. Do not use code fences.

## Target outcome

The result should read like a strong chapter summary that someone can review later to quickly recover the chapter's structure and key ideas without rereading the full detailed chapter export.

## Suggested structure

```markdown
# Chapter <N> Summary

## Chapter Thesis
A concise explanation of what this chapter is really doing.

## Structure Of The Chapter
- Subsection/grouping -> role in the chapter

## Core Ideas
- ...

## Important Mechanisms Or Frameworks
- ...

## Key Examples
- ...

## Caveats, Limitations, And Failure Modes
- ...

## Connections
- Links to previous chapters
- Dependencies for later chapters
- Reusable concept-note candidates

## What To Remember
- The highest-value takeaways from this chapter
```

## Quality bar

- Summarize at chapter level, not section level.
- Preserve signal, remove repetition.
- Keep enough detail that the summary is genuinely useful on its own.
