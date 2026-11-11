---
name: archive
description: Store private files in a local archive and restore them after a memory reset through catalog search. Use when deciding what to keep, searching or retrieving archived files, or deleting an archive entry; not for source control or storing secrets.
---

# Archive

The `archive` CLI stores private file bytes in a local store and records
only catalog metadata in a remote index. After a memory reset, search
the catalog and retrieve the file.

**The tool is not deployed yet.** The change that introduces this CLI is
still unmerged, and these commands have not been tested end to end. If
the `archive` command is missing or the store or index is unreachable,
report that limitation and stop. Do not invent a substitute store, and
do not claim that a file was stored or restored.

## Protect credentials

Configuration comes from the environment, or from a JSON file at
`~/.config/archive/config.json` (override the path with `ARCHIVE_CONFIG`).
The environment wins over the file; a blank variable is treated as
unset. Required values:

- `ARCHIVE_STORE_URL` / `storeUrl`
- `ARCHIVE_STORE_TOKEN` / `storeToken`
- `ARCHIVE_INDEX_URL` / `indexUrl`
- `ARCHIVE_INDEX_TOKEN` / `indexToken`

The store token and the index token are different secrets. The config
file should be mode 600; the CLI warns if group or other can read it.

Never print, echo, or log these environment values or the contents of
the config file. Never paste them into chats, pull requests, or
commits. If configuration is missing, name the missing variable or key
and stop. Do not dump the environment, read the file into the
conversation, or include URLs or tokens in a report.

Prefer `--json` on every command so success and failure are one JSON
object on stdout. Exit `0` is success, `1` is an operational error, and
`2` is a usage error. Do not add flags that are not listed here.

## Decide what to keep

Archive a file when it would change a later decision and is not already
durable in a repository or other system of record. Typical keepers are
accepted briefs, review evidence, decisions, notes, and diffs that an
agent would need after a memory reset.

Do not archive credentials, tokens, private keys, or other secrets.
Do not treat the archive as a backup of a git repository or as a place
to dump an entire transcript. Names are not unique, so give each put a
stable, searchable `--name`, relevant `--tags`, and a `--desc` (also
accepted as `--description`) that will still make sense without the
original conversation. `--notes` can hold longer context. Tags are
letters, numbers, and `._:-`, stored lowercase.

```
archive put <file> [--name name] [--tags a,b] [--desc text] [--notes text] [--mime type] --json
```

`put` uploads the bytes, checks the store's sha256 against a local hash,
then inserts the catalog row. If the insert fails, it tries to delete
the uploaded blob. The original local path is recorded on the row. The
store rejects uploads over its size cap (default 256 MiB). Record the
returned catalog id.

## Restore context after a memory reset

The agent may have no transcript. The catalog does.

```
archive search <query> --json
archive info <id> --json
archive get <id> -o ./restored-file --json
```

`search` is a case-insensitive substring match over name, path,
description, notes, tag, and id. `%` and `_` are literals. It returns
one page (default 50, maximum 200) and sets `truncated` when more
matched. `--limit` must be a positive integer and cannot exceed 200.

If you do not know what to search for, `archive ls --json` lists the
catalog, newest first. With no `--limit`, `ls` follows pages until the
catalog is exhausted, capped at 5000 rows, and sets `truncated` if more
remain. `--limit` requests a single page. `--tag` filters to one tag.

`info` and `get` accept a catalog id or an exact name. If several rows
share the name, they fail and list the ids unless you pass `--latest`
(newest `updatedAt`). Prefer the id from search or `ls`.

`get` writes into the working directory, using the last path segment of
the recorded path or the entry name, or to `-o path` (also `--output`).
It hashes the download and deletes the partial file if the sha256 or
size does not match the catalog. Downloads use the configured store
base plus the store id, not the URL stored on the row. `--force`
replaces an existing path. `-o -` writes raw bytes to stdout; with
`--json`, metadata goes to stderr so the pipe stays bytes. Prefer
`-o path --json` when both metadata and a file are needed.

If `get` reports a checksum mismatch, do not keep or trust the file.

## Delete safely

```
archive rm <id> --json
```

`rm` takes a catalog id only, never a name, so a shared name cannot
delete the wrong row. There is no confirmation prompt and no undelete.

Before `rm`, run `archive info <id> --json` and confirm the id, name,
and description are the intended row. Do not delete an entry without
explicit authorization, except to clean up a `put` you have just made
that clearly failed mid-way.

`rm` deletes the blob first, then the catalog row. A 404 from the store
counts as already gone, so a failed catalog delete can be retried. If
`rm` reports that the blob is gone but the catalog row remains, retry
`rm` with the same id. A crash between the two steps can leave a row
that points at a missing blob; `get` will then fail.
