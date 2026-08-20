# HTML report format

Render the review as one self-contained HTML file in the OS temp directory. Load Tailwind and Mermaid from CDNs. Use Mermaid for call graphs and dependencies. Use HTML and inline SVG for mass diagrams and cross-sections.

## HTML template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* styles not covered by Tailwind:
         dashed seam lines and arrowheads */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Show the repository name, date, and a compact legend. A solid box is a module. A dashed line is a seam. A red arrow is leakage. A thick dark box is a deep module. Skip the introduction and start with the candidates.

## Candidate card

Keep prose short. Let the diagrams show the structure. Use the terms from `$codebase-design`.

Each candidate uses one `<article>`:

- **Title.** Name the deepening in a few words, such as "Collapse the Order intake pipeline."
- **Badge row.** Show recommendation strength with `Strong` in emerald, `Worth exploring` in amber, or `Speculative` in slate. Add the dependency category: `in-process`, `local-substitutable`, `ports & adapters`, or `mock`.
- **Files.** Use a monospaced list with `font-mono text-sm`.
- **Before and after.** Put two diagrams side by side.
- **Problem.** State the concrete friction in one sentence.
- **Solution.** State the change in one sentence.
- **Wins.** Use at most six words per bullet, such as "Tests hit one interface" or "Delete four shallow wrappers."
- **ADR callout.** When relevant, use one line in an amber-tinted box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Choose the pattern that explains the candidate. Vary the diagrams when the structures differ.

### Mermaid graphs for dependencies and call flow

Use a Mermaid `flowchart` or `graph` for a call or dependency chain. Wrap it in a Tailwind card. Define classes that color leakage edges red and the deep module dark. Sequence diagrams work for comparisons such as six round trips before and one after.

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built boxes and arrows

Use bordered `<div>` elements for modules and inline SVG `<line>` or `<path>` elements for arrows when Mermaid cannot produce the layout. To show one deep module, use a thick outer border and fade its internal parts.

### Cross-section for layered shallowness

Stack horizontal bands with `h-12 border-l-4` to show the layers a call crosses. The before view might have six thin pass-through layers. The after view has one thick band labeled with the consolidated responsibility.

### Mass diagram for interface and implementation size

Draw two rectangles per module, one for the interface and one for the implementation. A shallow module has rectangles of similar height. A deep module has a short interface rectangle and a tall implementation rectangle.

### Collapsed call graph

Render the before view as a tree of nested function boxes. Collapse the same tree into one box for the after view, with internal calls faded inside it.

## Style guidance

- Use generous whitespace and little dashboard chrome. A serif heading font is optional.
- Use one accent color, such as emerald or indigo. Reserve red for leakage and amber for warnings.
- Keep diagrams near 320 pixels tall so both columns fit without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels. They should read as diagram labels, not interface controls.
- Load only the Tailwind CDN and Mermaid ESM scripts. The report has no other code or interaction.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Use plain, concise English. Keep the architecture nouns and verbs from `$codebase-design`.

**Use these terms:** module, interface, implementation, depth, deep, shallow, seam, adapter, locality.

**Do not substitute:** component, service, or unit for module; API or signature for interface; boundary for seam; layer or wrapper when you mean module.

**Phrases that fit:**

- "Order intake module is shallow. Its interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen it. One interface, one place to test."
- "Two adapters justify the seam: HTTP in production and in-memory in tests."

**Wins.** Name the concrete gain with glossary terms. Examples: *"locality: bugs stay in one module"*, *"one interface for N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Do not write *"easier to maintain"* or *"cleaner code"*. Those phrases do not explain what changed.

No hedging or throat-clearing. Cut phrases such as "it's worth noting that." If a sentence can be a bullet, make it one. If a bullet can be cut, cut it. Use the `$codebase-design` glossary before inventing another term.
