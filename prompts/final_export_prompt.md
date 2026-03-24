# Final Export Prompt

Use this at the end of a chapter study chat.

Your job is to produce a detailed markdown export that preserves the important knowledge from:

- the source chapter file
- the discussion in this chat
- clarifications, corrections, caveats, and examples that came up during study

The output is for long-term storage in Obsidian and must still be useful months later without reopening the original chat.

## Instructions

- Write a self-contained markdown note.
- Preserve important detail. Do not over-compress.
- Keep nuances, assumptions, tradeoffs, counterexamples, caveats, implementation notes, and edge cases.
- Include corrections made during the chat, especially where the original understanding changed.
- Preserve examples that materially improve understanding.
- Keep terminology precise.
- When the chat introduced useful reformulations or mental models, keep them.
- If the source chapter was ambiguous and the chat resolved that ambiguity, record the resolved interpretation and note that it was a clarification.
- If something remains uncertain, mark it clearly instead of smoothing it over.
- Prefer readable paragraphs and bullets over sparse fragments.
- Output only markdown. Do not wrap the result in code fences.

## Required output structure

```markdown
# <Chapter Note Title>

## Source
- Book:
- Chapter:
- Source pages:

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
- Include corrections, refinements, and distinctions that came from the chat.

## Terms And Definitions
- Term: definition

## Connections
- Link this chapter to earlier or later parts of the book when relevant.
- Mention concept-note candidates if they seem reusable beyond this book.

## Open Questions
- Only include real unresolved points.

## Practical Takeaways
- ...
```

## Quality bar

- The note should feel like a high-fidelity study export, not a compressed summary.
- Someone reading it later should understand both the source material and the most important value added by the discussion.
- Do not pad the note with generic prose.
- Do not drop important detail just to make it shorter.
