# Plan: <task>

Depth: tree <N>
Mode: orchestrated

## Contract

Fix these decisions before fan-out:

- Interfaces: <signatures, file formats, API shapes>
- File ownership: <files owned by each unit; concurrent units do not overlap>
- Conventions: <names, folders, error handling>

## Tree

- 1 <task>
  - 1.1 <branch> .......... gates/node-1.1.md
    - 1.1.1 <leaf> ........ gates/leaf-1.1.1.md
    - 1.1.2 <leaf> ........ gates/leaf-1.1.2.md
  - 1.2 <branch> .......... gates/node-1.2.md
    - 1.2.1 <leaf> ........ gates/leaf-1.2.1.md
    - 1.2.2 <leaf> ........ gates/leaf-1.2.2.md

## Dispatch graph

A unit is ready when every dependency below is verified. `none` means it is
ready at the first dispatch. Concurrently ready units must own different
files.

| Unit | Kind | Depends on | Owns | Gates |
|---|---|---|---|---|
| 1.1.1 | leaf | none | <files> | gates/leaf-1.1.1.md |
| 1.1.2 | leaf | none | <files> | gates/leaf-1.1.2.md |
| 1.1 | integration | 1.1.1, 1.1.2 | <integration files> | gates/node-1.1.md |
| 1.2.1 | leaf | none | <files> | gates/leaf-1.2.1.md |
| 1.2.2 | leaf | <unit IDs, or none> | <files> | gates/leaf-1.2.2.md |
| 1.2 | integration | 1.2.1, 1.2.2 | <integration files> | gates/node-1.2.md |
| 1 | integration | 1.1, 1.2 | <root integration files> | <root gates file> |

## Status log

Append-only. Record dispatch, return, parent verification, retry, newly ready
units, and abandoned gates. Never rewrite earlier lines.

- <timestamp or step> plan written, contract fixed
