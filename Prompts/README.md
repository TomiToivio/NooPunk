# Tomi's NoöPunk prompt archive

This directory preserves Tomi's **substantial original NoöPunk design and development prompts**. The goal is to keep background material, rules, theoretical ideas and abandoned concepts recoverable, without turning the repository into a chat log.

**Canon boundary:** an archived prompt is evidence of what Tomi once proposed, not approved canon, a current implementation instruction, or a licence to change CWN/SWN/AWN/WWN rules. Current scope gates still apply.

## What qualifies

Log a prompt when all of these are true:

- it is clearly about NoöPunk **Story**, **Simulator** or **RPG** (the three subprojects overlap, so one directory is correct);
- it contains considerable original background, design, rules, theory or development ideas;
- it is long/substantive enough that Tomi visibly invested effort writing it.

Use qualitative judgment. There is no rigid word cutoff; a short but unusually dense design note may qualify, and a long routine thread may not.

## What does not qualify

Do **not** log:

- short or routine requests: "do this", "fix this", PR merges, status questions, "continue";
- casual recommendations or questions such as "what is the best NoöPunk movie?";
- unrelated projects;
- agent answers, summaries or generated text as if they were Tomi's prompt;
- hidden context, other users' messages, credentials or incidental private information.

## Privacy

Archive only the explicitly supplied relevant NoöPunk author prompt — not hidden context, other users' messages, credentials or incidental private information. If a design prompt contains a secret or private identifier, redact it with a clear note instead of publishing it.

## Filename convention

```
Prompts/DD_MM_YYYY_TOPIC_NAME.md
```

- `DD_MM_YYYY` is the date of the original prompt, zero-padded.
- `TOPIC_NAME` is a short uppercase underscore-separated description, for example `07_11_2026_PROMPT_LOGGING.md`.
- For multiple distinct prompts on the same date and topic, add a meaningful suffix (for example `_PART_2` or `_FOLLOWUP`). Do not overwrite a different prompt.
- Preserve the prompt's source language. Do not translate or "correct" Tomi's wording.

## Duplicate and normalization rules

Before adding a file:

1. Scan `Prompts/` by date, topic and key phrases, and check whether the same prompt is already saved elsewhere in the repository.
2. If the same prompt exists under a nonstandard filename, move/rename it to the convention while preserving its content and history where possible.
3. If a standardized file already holds the same prompt, do not duplicate it.
4. If Tomi edited a prompt after the first archive, preserve both versions faithfully with source/date labels, or use separate descriptive filenames. Do not silently replace the older wording.

## File shape

A short header is fine:

```markdown
# Prompt: <short title>

- **Date:** YYYY-MM-DD
- **Topic:** <topic>
- **Source:** <where the prompt was written, if known>
- **Archive status:** Original author prompt; not canon or an approved implementation specification.

## Original prompt (verbatim text, Markdown formatting normalized)

<the author's actual text>
```

Do not paraphrase the prompt body. Markdown formatting may be normalized for readability, but wording, examples, links and abandoned ideas must remain.

## When to archive

Archive as part of handling a qualifying prompt — do not wait for a separate request. Check for duplicates first, add or normalize the file in the same documentation-only change where feasible, and link it from the related issue/PR when useful.

This is documentation only. It does not authorize new RPG, Story or Simulator feature development, does not reopen deferred issues, and does not change the active scope gate in [`AGENTS.md`](../AGENTS.md).

## Index

| Date | Topic | File |
| --- | --- | --- |
| 2026-11-07 | Prompt logging | [`07_11_2026_PROMPT_LOGGING.md`](07_11_2026_PROMPT_LOGGING.md) |
