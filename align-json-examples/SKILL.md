---
name: align-json-examples
description: Format and vertically align JSON or JSONC examples in Markdown, Notion pages, specifications, and chat. Use when the user asks to format JSON code blocks, align field values, align inline comments, clean up API request or response examples, or apply the aligned JSON style used in technical documents.
---

# Align JSON examples

Format JSON examples for scanning, then align sibling values and inline comments. Preserve every key, value, key order, and comment.

Use the bundled formatter:

```bash
python3 <skill-directory>/scripts/align_json_examples.py <file>
```

It supports raw JSONC and Markdown containing fenced `json` or `jsonc` blocks. A block may contain multiple top-level request and response objects separated by comments or blank lines.

## Required style

- Use two spaces per nesting level.
- Put one property on each line.
- Start sibling values in the same column.
- Start sibling `//` comments in the same column, two spaces after the longest property line.
- Treat each nested object as its own alignment group.
- Expand a one-line nested object when its fields need alignment.
- Keep request, response, and event examples separated by a blank line and a short comment.
- Preserve key order. Never sort fields while formatting documentation.
- Do not add trailing commas.
- Keep a comment on the field it describes.

Example:

```jsonc
{
  "id":         "7",  // ClassPass identifier
  "long_field": 42    // Number of attempts
}
```

Comments make an example JSONC even when an existing documentation system labels the fence `json`. Never send comments in an actual JSON API payload.

## Workflow

1. Collect every affected `json` and `jsonc` block. Do not format only the visibly misaligned block when the user asked for the whole document.
2. Run the formatter on a local copy or pipe a raw snippet through it.
3. Use `--expand-inline-objects` when compact nested objects prevent vertical field alignment.
4. Review the output for domain-specific grouping. Formatting must not rename fields, change enum casing, alter values, or reorder keys.
5. Apply the exact formatted blocks to the source document.
6. Re-read the source and run `--check` against the resulting local copy.
7. Confirm that sibling value columns and sibling comment columns are aligned and that all original comments and parsed values remain.

## Commands

Format to standard output:

```bash
python3 <skill-directory>/scripts/align_json_examples.py example.jsonc
```

Format every JSON fence in Markdown:

```bash
python3 <skill-directory>/scripts/align_json_examples.py design.md
```

Expand compact nested objects and update a file:

```bash
python3 <skill-directory>/scripts/align_json_examples.py design.md \
  --expand-inline-objects \
  --write
```

Check formatting without changing the file:

```bash
python3 <skill-directory>/scripts/align_json_examples.py design.md \
  --expand-inline-objects \
  --check
```

Run the formatter's built-in behavioral checks:

```bash
python3 <skill-directory>/scripts/align_json_examples.py --self-test
```

## Notion pages

Fetch the page as enhanced Markdown. Extract all fenced `json` and `jsonc` blocks, format them together, then replace each old block with its formatted form using exact-content updates. Re-fetch the page and verify:

- the number of fenced blocks is unchanged;
- the number of top-level JSON objects and arrays is unchanged;
- parsed values and key order are unchanged;
- the ordered list of `//` comments is unchanged;
- every sibling value column is identical;
- every sibling inline-comment column is identical.

Do not rewrite surrounding prose or diagrams as part of formatting.

## Safety boundaries

The formatter accepts strict JSON plus `//` comments. It intentionally rejects block comments, malformed delimiters, unparseable values, and trailing-comma JSONC rather than guessing. Split unsupported examples or normalize them with a syntax-aware JSONC parser before alignment.

The formatter validates semantic values, key order, and comments before returning output. Treat any validation failure as a blocker. Do not fall back to regex replacement or manual global whitespace edits.
