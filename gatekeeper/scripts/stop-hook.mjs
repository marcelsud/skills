#!/usr/bin/env node
// Claude Code Stop hook for Gatekeeper.
//
// Blocks the turn while GATES.md or gates/*.md has unmet gates. This file
// scan uses no model call.
//
// Behavior:
//   - No gate files                         -> allow
//   - Invalid or empty gate file            -> block with the parse error
//   - All gates met or abandoned           -> allow
//   - Unmet gates with recent file changes -> block with one reason
//   - Unmet gates unchanged for MAX_BLOCKS -> allow with a warning
//
// Claude Code also releases after 8 consecutive blocks.
// Progress means the combined gate-file content changed after the last block.
// State is stored in .gatekeeper-hook-state.json beside the gates.
//
// Hook contract: code.claude.com/docs/en/hooks
//   stdin  JSON with { cwd, stop_hook_active, ... }
//   stdout block JSON plus exit 0, or no output plus exit 0 to allow

import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { createHash } from "node:crypto";

const MAX_BLOCKS = 6;

function readStdin() {
  try { return readFileSync(0, "utf8"); } catch { return "{}"; }
}

let payload = {};
try { payload = JSON.parse(readStdin() || "{}"); } catch { /* stay permissive */ }
const cwd = payload.cwd || process.cwd();

function gateFiles(dir) {
  const found = [];
  const top = join(dir, "GATES.md");
  if (existsSync(top)) found.push(top);
  const gdir = join(dir, "gates");
  if (existsSync(gdir)) {
    try {
      for (const f of readdirSync(gdir)) if (f.endsWith(".md")) found.push(join(gdir, f));
    } catch { /* ignore */ }
  }
  return found;
}

const files = gateFiles(cwd);
if (!files.length) process.exit(0); // no gates, nothing to enforce

const GATE_RE = /^- \[( |x|X)\] (.*)$/;
const GATE_LIKE_RE = /^\s*[-*]\s*\[[^\]]*\]/;
const EVIDENCE_RE = /^\s+EVIDENCE:\s?(.*)$/;
const ABANDON_RE = /^ABANDON:\s*(\S+)/;

let combined = "";
const unmet = [];
const parseErrors = [];

for (const file of files) {
  let text = "";
  try {
    text = readFileSync(file, "utf8");
  } catch (error) {
    parseErrors.push(`${file}: cannot read (${error.message})`);
    continue;
  }
  combined += text;
  const lines = text.split(/\r?\n/);
  const abandoned = new Set(
    lines.map(l => (l.match(ABANDON_RE) || [])[1]).filter(Boolean).map(s => s.replace(/:$/, ""))
  );
  let cur = null;
  let gateCount = 0;
  const flush = () => {
    if (!cur || abandoned.has(cur.id)) { cur = null; return; }
    const pending = cur.evidence === null || /^pending$/i.test(cur.evidence);
    if (!cur.checked || pending) unmet.push(cur.id);
    cur = null;
  };
  lines.forEach((line, index) => {
    const g = line.match(GATE_RE);
    if (!g && GATE_LIKE_RE.test(line)) {
      parseErrors.push(`${file}:${index + 1}: malformed gate checkbox`);
    }
    if (g) {
      flush();
      gateCount++;
      cur = {
        checked: g[1].toLowerCase() === "x",
        id: (g[2].match(/^(\S+?):/) || [null, g[2].trim().slice(0, 24)])[1],
        evidence: null,
      };
      return;
    }
    const ev = cur && line.match(EVIDENCE_RE);
    if (ev) cur.evidence = ev[1].trim();
  });
  flush();
  if (gateCount === 0) parseErrors.push(`${file}: no gates found`);
}

const issues = [...parseErrors, ...unmet];
if (!issues.length) process.exit(0); // All gates met or abandoned.

// Release the hook after repeated blocks with no gate-file change.
const statePath = join(cwd, ".gatekeeper-hook-state.json");
const hash = createHash("sha256").update(combined).digest("hex").slice(0, 16);
let state = { hash: "", blocks: 0 };
try { state = JSON.parse(readFileSync(statePath, "utf8")); } catch { /* fresh */ }
if (state.hash !== hash) state = { hash, blocks: 0 }; // Reset after progress.
state.blocks += 1;
try { writeFileSync(statePath, JSON.stringify(state)); } catch { /* non-fatal */ }

if (state.blocks > MAX_BLOCKS) {
  // Release after MAX_BLOCKS unchanged stops.
  console.log(JSON.stringify({
    systemMessage: `gatekeeper: releasing after ${MAX_BLOCKS} blocks without gate progress; ${issues.length} issue(s) remain (${issues.slice(0, 4).join(", ")}).`,
  }));
  process.exit(0);
}

const list = issues.slice(0, 5).join(", ") + (issues.length > 5 ? `, +${issues.length - 5} more` : "");
const reason = parseErrors.length > 0
  ? `gatekeeper: invalid gate file(s): ${list}. Fix the gate syntax before stopping.`
  : `gatekeeper: ${unmet.length} gate(s) unmet: ${list}. Run gate-check.mjs, then work the next unmet gate. If an external blocker makes a gate impossible, add "ABANDON: <id> <reason>". Finish only when every remaining gate has evidence.`;
console.log(JSON.stringify({
  decision: "block",
  reason,
}));
process.exit(0);
