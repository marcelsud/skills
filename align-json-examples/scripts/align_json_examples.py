#!/usr/bin/env python3
"""Format JSON examples and align sibling values and // comments."""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROPERTY_RE = re.compile(r'^(\s*)("(?:[^"\\]|\\.)+":)\s*(.+)$')
FENCE_RE = re.compile(
    r"^(?P<indent>[ \t]*)```(?P<language>jsonc?)[ \t]*\n"
    r"(?P<body>.*?)"
    r"^(?P=indent)```[ \t]*$",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)


@dataclass
class Property:
    line_index: int
    object_id: int
    prefix: str
    value: str
    comment: str | None
    aligned_code: str = ""


def split_inline_comment(line: str) -> tuple[str, str | None]:
    """Split a // comment while ignoring // inside a JSON string."""
    in_string = False
    escaped = False
    index = 0
    while index < len(line) - 1:
        character = line[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif character == "/" and line[index + 1] == "/":
            return line[:index].rstrip(), line[index:].strip()
        index += 1
    return line.rstrip(), None


def structural_tokens(line: str) -> list[str]:
    """Return object and array delimiters outside strings and comments."""
    code, _ = split_inline_comment(line)
    tokens = []
    in_string = False
    escaped = False
    for character in code:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif character in "{}[]":
            tokens.append(character)
    return tokens


def normalize_indentation(text: str) -> str:
    """Apply two-space structural indentation without changing tokens."""
    depth = 0
    output = []
    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            output.append("")
            continue

        tokens = structural_tokens(stripped)
        starts_with_close = stripped[0] in "}]"
        line_depth = depth - 1 if starts_with_close else depth
        if line_depth < 0:
            raise ValueError(f"unexpected closing delimiter on line {line_number}")
        output.append("  " * line_depth + stripped)

        for token in tokens:
            if token in "{[":
                depth += 1
            else:
                depth -= 1
                if depth < 0:
                    raise ValueError(f"unexpected closing delimiter on line {line_number}")

    if depth:
        raise ValueError("unclosed JSON object or array")
    return "\n".join(output)


def expand_inline_object_properties(text: str) -> str:
    """Expand one-line object property values while preserving their comments."""
    output = []
    for line in text.splitlines():
        code, comment = split_inline_comment(line)
        match = PROPERTY_RE.match(code)
        if not match:
            output.append(line.rstrip())
            continue

        indent, key, value = match.groups()
        trailing_comma = value.endswith(",")
        candidate = value[:-1].rstrip() if trailing_comma else value.rstrip()
        if not (candidate.startswith("{") and candidate.endswith("}")):
            output.append(line.rstrip())
            continue

        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            output.append(line.rstrip())
            continue
        if not isinstance(parsed, dict) or not parsed:
            output.append(line.rstrip())
            continue

        rendered = json.dumps(parsed, ensure_ascii=False, indent=2).splitlines()
        opening = f"{indent}{key} {{"
        if comment:
            opening += f"  {comment}"
        output.append(opening)
        output.extend(indent + rendered_line for rendered_line in rendered[1:-1])
        output.append(f"{indent}}}{',' if trailing_comma else ''}")
    return "\n".join(output)


def align_properties(text: str) -> str:
    """Align value and comment columns independently within each object."""
    lines = text.splitlines()
    context_stack: list[tuple[str, int]] = []
    next_context_id = 0
    properties: list[Property] = []

    for line_index, line in enumerate(lines):
        code, comment = split_inline_comment(line)
        match = PROPERTY_RE.match(code)
        if match:
            if not context_stack or context_stack[-1][0] != "{":
                raise ValueError(f"property outside an object on line {line_index + 1}")
            indent, key, value = match.groups()
            properties.append(
                Property(
                    line_index=line_index,
                    object_id=context_stack[-1][1],
                    prefix=indent + key,
                    value=value.strip(),
                    comment=comment,
                )
            )

        for token in structural_tokens(line):
            if token in "{[":
                next_context_id += 1
                context_stack.append((token, next_context_id))
                continue
            expected = "{" if token == "}" else "["
            if not context_stack or context_stack[-1][0] != expected:
                raise ValueError(f"mismatched delimiter on line {line_index + 1}")
            context_stack.pop()

    if context_stack:
        raise ValueError("unclosed JSON object or array")

    by_object: dict[int, list[Property]] = {}
    for prop in properties:
        by_object.setdefault(prop.object_id, []).append(prop)

    for siblings in by_object.values():
        value_column = max(len(prop.prefix) for prop in siblings) + 1
        for prop in siblings:
            prop.aligned_code = (
                prop.prefix + " " * (value_column - len(prop.prefix)) + prop.value
            )
        comment_column = max(len(prop.aligned_code) for prop in siblings) + 2
        for prop in siblings:
            line = prop.aligned_code
            if prop.comment:
                line += " " * (comment_column - len(line)) + prop.comment
            lines[prop.line_index] = line

    return "\n".join(lines)


def root_value_spans(text: str) -> list[tuple[int, int]]:
    """Find multiple top-level object or array values in JSONC text."""
    spans = []
    stack: list[str] = []
    start = None
    in_string = False
    escaped = False
    in_comment = False
    index = 0

    while index < len(text):
        character = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if in_comment:
            if character == "\n":
                in_comment = False
            index += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            index += 1
            continue
        if character == "/" and following == "/":
            in_comment = True
            index += 2
            continue
        if character == '"':
            in_string = True
        elif character in "{[":
            if not stack:
                start = index
            stack.append(character)
        elif character in "}]":
            expected = "{" if character == "}" else "["
            if not stack or stack[-1] != expected:
                raise ValueError("mismatched JSON delimiter")
            stack.pop()
            if not stack and start is not None:
                spans.append((start, index + 1))
                start = None
        index += 1

    if stack or in_string:
        raise ValueError("incomplete JSON value")
    return spans


def remove_line_comments(text: str) -> str:
    return "\n".join(split_inline_comment(line)[0] for line in text.splitlines())


def semantic_values(text: str):
    """Parse roots with ordered object pairs so key order is part of validation."""
    values = []
    for start, end in root_value_spans(text):
        values.append(
            json.loads(
                remove_line_comments(text[start:end]),
                object_pairs_hook=lambda pairs: ("__object__", pairs),
            )
        )
    if not values:
        raise ValueError("no JSON object or array found")
    return values


def line_comments(text: str) -> list[str]:
    comments = []
    for line in text.splitlines():
        _, comment = split_inline_comment(line)
        if comment:
            comments.append(comment)
    return comments


def format_jsonc(text: str, *, expand_inline_objects: bool = False) -> str:
    """Format one JSONC example or a block containing several root values."""
    if "/*" in text or "*/" in text:
        raise ValueError("block comments are unsupported; use // comments")

    original_values = semantic_values(text)
    original_comments = line_comments(text)
    formatted = text.strip("\n")
    if expand_inline_objects:
        formatted = expand_inline_object_properties(formatted)
    formatted = normalize_indentation(formatted)
    formatted = align_properties(formatted)

    if semantic_values(formatted) != original_values:
        raise ValueError("formatting changed JSON values or key order")
    if line_comments(formatted) != original_comments:
        raise ValueError("formatting changed comments")
    return formatted


def format_markdown(text: str, *, expand_inline_objects: bool = False) -> str:
    """Format every fenced json or jsonc block in Markdown."""
    count = 0

    def replace(match: re.Match) -> str:
        nonlocal count
        count += 1
        indent = match.group("indent")
        language = match.group("language")
        body = format_jsonc(
            match.group("body").rstrip("\n"),
            expand_inline_objects=expand_inline_objects,
        )
        return f"{indent}```{language}\n{body}\n{indent}```"

    formatted = FENCE_RE.sub(replace, text)
    if not count:
        raise ValueError("no fenced json or jsonc blocks found")
    return formatted


def format_input(text: str, path: Path | None, expand_inline_objects: bool) -> str:
    markdown = bool(FENCE_RE.search(text)) or bool(path and path.suffix.lower() in {".md", ".mdx"})
    if markdown:
        return format_markdown(text, expand_inline_objects=expand_inline_objects)
    return format_jsonc(text, expand_inline_objects=expand_inline_objects) + "\n"


def alignment_columns(text: str) -> tuple[bool, bool]:
    """Return whether sibling value and comment columns are aligned."""
    lines = text.splitlines()
    context_stack: list[tuple[str, int]] = []
    next_context_id = 0
    groups: dict[int, list[tuple[int, int | None]]] = {}

    for line in lines:
        code, comment = split_inline_comment(line)
        match = PROPERTY_RE.match(code)
        if match:
            indent, key, spacing, value = re.match(
                r'^(\s*)("(?:[^"\\]|\\.)+":)(\s+)(.+)$', code
            ).groups()
            value_column = len(indent + key + spacing)
            comment_column = line.index("//", value_column) if comment else None
            groups.setdefault(context_stack[-1][1], []).append(
                (value_column, comment_column)
            )
        for token in structural_tokens(line):
            if token in "{[":
                next_context_id += 1
                context_stack.append((token, next_context_id))
            else:
                context_stack.pop()

    values_aligned = all(len({value for value, _ in group}) == 1 for group in groups.values())
    comments_aligned = all(
        len({comment for _, comment in group if comment is not None}) <= 1
        for group in groups.values()
    )
    return values_aligned, comments_aligned


def self_test() -> None:
    raw = '''// request
{
"id":"1",// identifier
"long_name": 2 // count
}

// response
{
"subject":{"user_id":"7","venue_id":"9"}, // subject
"source":"magicline" // integration
}'''
    expected = '''// request
{
  "id":        "1",  // identifier
  "long_name": 2     // count
}

// response
{
  "subject": {            // subject
    "user_id":  "7",
    "venue_id": "9"
  },
  "source":  "magicline"  // integration
}'''
    actual = format_jsonc(raw, expand_inline_objects=True)
    assert actual == expected, actual
    assert alignment_columns(actual) == (True, True)

    markdown = f"before\n\n```jsonc\n{raw}\n```\n\nafter\n"
    formatted_markdown = format_markdown(markdown, expand_inline_objects=True)
    assert expected in formatted_markdown
    assert formatted_markdown.startswith("before\n")
    assert formatted_markdown.endswith("\nafter\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="JSONC or Markdown file; defaults to stdin")
    output_mode = parser.add_mutually_exclusive_group()
    output_mode.add_argument("--write", action="store_true", help="replace the input file")
    output_mode.add_argument("--check", action="store_true", help="exit 1 when formatting differs")
    parser.add_argument(
        "--expand-inline-objects",
        action="store_true",
        help="expand one-line object property values before alignment",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("ok")
        return 0
    if args.write and not args.input:
        parser.error("--write requires an input path")

    text = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    formatted = format_input(text, args.input, args.expand_inline_objects)

    if args.check:
        if formatted != text:
            print(f"needs formatting: {args.input or '<stdin>'}", file=sys.stderr)
            return 1
        print("ok")
        return 0
    if args.write:
        args.input.write_text(formatted, encoding="utf-8")
        return 0
    sys.stdout.write(formatted)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
