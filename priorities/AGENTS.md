# Priorities Project Agent Guide

This directory is the dedicated project area for a local-first priorities tool for JangaFX managers.

The next agent should treat this file as the implementation brief and follow it in order. Do not redesign the product unless the user explicitly asks. Keep the stack minimal. Keep the data human-readable. Keep the UX calm and thoughtful.

## Mission

Build a macOS-first, local-first priorities tool inspired by Obsidian and informed by Shape Up.

The tool must help a manager:

- capture possible priorities
- shape them into clearer bets
- compare them using multiple prioritization frameworks
- estimate cost/effort at a lightweight level
- reason about team fit based on developer strengths
- publish a clear "why these, why now" brief for the team

## Locked Decisions

These are already decided. Do not reopen them unless the user asks.

- Platform strategy: build in a dev-friendly way first, package later.
- OS target: macOS first.
- Audience: manager-first, single-user at first, with at least one additional manager later.
- Data store: plain Markdown files are the source of truth.
- Database: none.
- App model: local-first.
- Product style: Obsidian-inspired, text-first, durable, private, minimal.
- Editing model: hybrid.
  - Narrative sections should feel like writing notes.
  - Structured fields should have better controls.
- Status model:
  - `backlog`
  - `todo`
  - `working`
  - `cancelled`
  - `done`
- Priority frameworks to support in v1:
  - `Shape Up` as the required narrative backbone
  - `RICE` as an optional comparison lens
  - `ICE` as an optional comparison lens
  - `Cost of Delay vs Effort` as an optional comparison lens
  - `Strategic Alignment` as a required score
  - `Confidence` as a required score
  - `Team Fit` as a required score

## Product Principles

- Files first, app second.
- The filesystem is the product; the UI is a helper.
- Raw files must remain readable and useful outside the app.
- Do not build a generic project tracker.
- Do not build Agile mechanics, sprint tools, or task micromanagement.
- Frameworks help judgment; they do not replace judgment.
- Avoid fake precision.
- Prefer a small number of strong primitives over many features.

## Non-Goals For V1

Do not build these yet:

- auth
- sync
- cloud hosting
- collaboration
- comments
- notifications
- plugins
- graph view
- rich text editor
- database or search index
- task/subtask tracking
- sprint boards
- story points

## Minimal Stack

Use the smallest practical stack.

- Runtime: `Node.js`
- Language: `TypeScript`
- Server: Node built-in `http` module first; do not add a web framework unless absolutely necessary.
- Rendering: server-rendered HTML with plain CSS and only small amounts of vanilla JavaScript.
- Markdown/frontmatter: `gray-matter` and `marked`
- Validation: `zod`
- Development runner: `tsx`
- Types: `@types/node`
- Tests: use Node built-in `node:test` if tests are added

Do not add React, Next.js, Tailwind, a database, an ORM, or any extra libraries unless the user asks or there is a strong reason.

## Why Each Dependency Exists

Keep these explanations in mind if the user asks again.

- `TypeScript`: catches mistakes and keeps the code maintainable.
- `tsx`: lets the app run TypeScript directly in development without extra ceremony.
- `gray-matter`: reads YAML frontmatter from Markdown files.
- `marked`: turns Markdown into browser-readable HTML.
- `zod`: validates file structure so broken notes fail clearly.
- `@types/node`: gives TypeScript the Node API types.

## Initial Development Model

During development, the app should run locally with simple commands:

```bash
npm install
npm run dev
```

The app should then open locally in a browser. Packaging into a desktop app is a later phase and must not require a rewrite of the data model or app logic.

## Required Directory Structure

Create and maintain this structure:

```text
priorities/
  AGENTS.md
  package.json
  tsconfig.json
  .gitignore
  src/
    server.ts
    types.ts
    lib/
      content.ts
      frontmatter.ts
      markdown.ts
      sections.ts
      scores.ts
      files.ts
      paths.ts
    views/
      layout.ts
      home.ts
      priorities.ts
      people.ts
      cycles.ts
      compare.ts
    public/
      app.css
      app.js
  content/
    priorities/
    people/
    cycles/
    templates/
```

Notes:

- `content/` is the default local vault for development.
- Keep the code organized so a future external vault path can be added without a large refactor.
- Keep route/view logic separate from file parsing and scoring logic.

## Data Model Rules

Markdown files are canonical. Every important piece of data must round-trip cleanly to Markdown.

### Priority Note Rules

- File name: `<id>.md`
- `id` must be a stable slug.
- Use fixed body headings for consistency.
- Frontmatter is for structured metadata.
- Body is for narrative content.

Use this exact frontmatter shape for priorities:

```md
---
id: improve-onboarding
title: Improve onboarding
status: backlog
tags:
  - ux
  - onboarding
owners:
  - alice
cycle:
appetite: 4 weeks
scores:
  strategic_alignment: 4
  confidence: 3
  team_fit: 5
frameworks:
  rice:
    reach: 4
    impact: 5
    confidence: 3
    effort: 2
  ice:
    impact: 5
    confidence: 3
    ease: 4
  delay_effort:
    cost_of_delay: 4
    effort: 2
---

## Problem

## Why Now

## Desired Outcome

## Boundaries

## Risks

## Staffing Notes

## Decision Rationale
```

Priority rules:

- `status` must be one of the locked values.
- `tags` and `owners` default to empty arrays.
- `cycle` may be blank.
- `appetite` stays as plain text for now.
- `scores.strategic_alignment`, `scores.confidence`, and `scores.team_fit` are required 1-5 integers.
- `frameworks` entries are optional. If absent, the app should still work.
- All framework inputs use simple 1-5 integer scales in v1.
- This is an intentionally simplified adaptation so the UI stays lightweight and the data stays easy to reason about.

### Person Note Rules

- File name: `<id>.md`
- `id` must be a stable slug.

Use this exact frontmatter shape for people:

```md
---
id: alice
name: Alice Example
role: Senior Graphics Engineer
strengths:
  - rendering
  - architecture
interests:
  - tooling
  - onboarding
domains:
  - embergen
  - internal-tools
load: medium
tags:
  - frontend
  - engine
---

## Summary

## Strengths

## Interests

## Constraints

## Notes
```

Person rules:

- `load` should be a simple string for now, such as `low`, `medium`, or `high`.
- Keep this human and lightweight. Do not turn it into HR software.

### Cycle Note Rules

- File name: `<id>.md`
- `id` must be a stable slug.

Use this exact frontmatter shape for cycles:

```md
---
id: 2026-cycle-2
title: 2026 Cycle 2
start_date: 2026-04-06
end_date: 2026-05-15
tags:
  - q2
---

## Focus

## Why This Cycle

## Team Brief

## Notes
```

Cycle rules:

- A cycle note holds the narrative for that cycle.
- Priority notes may reference a cycle by `id` using the `cycle` field.
- Do not duplicate priority membership in both places.

## Note Parsing Rules

- Body headings are fixed in v1.
- Parse narrative sections by heading.
- Preserve heading order when serializing back to disk.
- If a section is missing, treat it as empty and repair it on save.
- Do not introduce a rich text format.
- The raw Markdown must remain pleasant to read directly.

## Scoring Rules

The app must support multiple comparison lenses while remaining simple.

### Required Always-On Scores

- `Strategic Alignment` -> 1-5 integer
- `Confidence` -> 1-5 integer
- `Team Fit` -> 1-5 integer

These should always appear on every priority.

### Optional Framework Lenses

- `RICE`
  - simplified v1 formula: `(reach * impact * confidence) / effort`
- `ICE`
  - simplified v1 formula: `impact * confidence * ease`
- `Cost of Delay vs Effort`
  - simplified v1 formula: `cost_of_delay / effort`

Important:

- Keep formulas transparent in the UI.
- Show raw inputs and computed scores together.
- Allow priorities with no optional framework data.
- Final ranking must support manual judgment and written rationale.

## Team Fit Rules

The app must help suggest likely owners without pretending certainty.

- Match priority tags, owners, and narrative content against person strengths, interests, and domains.
- Start with a simple heuristic, not AI.
- Prefer clear explainability over cleverness.
- Show suggested people and why they appear.
- Keep manual editing easy.

## UX Direction

The app should feel closer to a thoughtful knowledge tool than an enterprise dashboard.

- Calm, local, text-first layout.
- Reading and writing should feel central.
- Structured metadata should be easier to edit than raw YAML.
- Use simple forms for frontmatter-backed fields.
- Use textareas for narrative sections.
- Render Markdown for reading views.
- Checklists in Markdown may become clickable as progressive enhancement, but raw Markdown stays canonical.
- Tags should render as discrete chips.
- Owner and cycle references should be clickable.
- Favor clarity, whitespace, and hierarchy over dense control panels.

## Route Plan For V1

Implement these pages first:

- `/` -> simple home/dashboard view
- `/priorities` -> list all priorities
- `/priorities/new` -> create a priority
- `/priorities/:id` -> read a priority
- `/priorities/:id/edit` -> edit a priority
- `/compare` -> compare 2 or more priorities side by side
- `/people` -> list people
- `/people/:id` -> read a person note
- `/cycles` -> list cycles
- `/cycles/:id` -> read a cycle and its related priorities

Optional after the above:

- `/brief/current` -> current team-facing priorities brief

## Execution Order

Follow these phases in order. Do not jump ahead to packaging, advanced interactivity, or visual polish before the foundations exist.

### Phase 1: Scaffold The Project

Do this first.

1. Create `package.json`.
2. Add scripts:
   - `dev`
   - `build`
   - `start`
   - `check`
3. Add dependencies:
   - `gray-matter`
   - `marked`
   - `zod`
4. Add dev dependencies:
   - `typescript`
   - `tsx`
   - `@types/node`
5. Create `tsconfig.json` with strict TypeScript settings.
6. Create `.gitignore` for `node_modules`, `dist`, and local temp files.
7. Create the `src/` and `content/` directories from the structure above.
8. Create starter sample files in `content/priorities`, `content/people`, and `content/cycles`.
9. Create starter templates in `content/templates`.

Acceptance check for Phase 1:

- `npm install` works.
- `npm run check` works.
- The repository has the intended structure.

### Phase 2: Build The Content Layer

This phase defines the real foundation.

1. Implement TypeScript types for priority, person, cycle, and score objects.
2. Implement `zod` schemas matching the Markdown rules in this file.
3. Implement frontmatter parsing with `gray-matter`.
4. Implement fixed-section parsing for Markdown bodies.
5. Implement serializers that round-trip cleanly back to Markdown.
6. Implement file listing and file loading helpers.
7. Implement load-all helpers for priorities, people, and cycles.
8. Implement safe save helpers for create/update flows.
9. Implement score calculation helpers for the optional frameworks.

Acceptance check for Phase 2:

- Sample notes load successfully.
- Broken notes fail with clear messages.
- Saving a note preserves readability and heading order.
- Score helpers produce deterministic results.

### Phase 3: Build The App Shell

1. Implement `src/server.ts` using Node `http`.
2. Implement a small router by hand.
3. Implement a shared layout renderer.
4. Add a single CSS file in `src/public/app.css`.
5. Serve static files from `src/public`.
6. Add a minimal home page that links to priorities, people, cycles, and compare.

Acceptance check for Phase 3:

- `npm run dev` starts the app locally.
- The home page loads.
- Navigation works.

### Phase 4: Implement Priority Pages

1. Build `/priorities` list view.
2. Add filtering by status.
3. Add filtering by cycle and tag if simple to do.
4. Build `/priorities/:id` read view.
5. Render frontmatter-backed structured fields clearly.
6. Render body sections using Markdown.
7. Build `/priorities/new` form.
8. Build `/priorities/:id/edit` form.
9. Use simple form controls for structured data:
   - status select
   - tag inputs
   - owner multi-select or simple token input
   - cycle select
   - score inputs
10. Use textareas for narrative sections.

Acceptance check for Phase 4:

- A new priority can be created.
- An existing priority can be edited.
- The saved file is readable Markdown.
- Status changes appear correctly in the list.

### Phase 5: Implement Comparison Views

1. Build `/compare`.
2. Allow selecting multiple priorities.
3. Show side-by-side comparisons for:
   - status
   - appetite
   - strategic alignment
   - confidence
   - team fit
   - optional RICE
   - optional ICE
   - optional delay vs effort
4. Show formulas and computed scores plainly.
5. Highlight missing data without breaking the page.
6. Include the narrative fields needed for judgment, especially:
   - Problem
   - Why Now
   - Desired Outcome
   - Risks
   - Decision Rationale

Acceptance check for Phase 5:

- Two or more priorities can be compared.
- Missing framework data is handled gracefully.
- The page helps a manager explain tradeoffs.

### Phase 6: Implement People And Team Fit

1. Build `/people` list view.
2. Build `/people/:id` read view.
3. Parse strengths, interests, domains, load, and notes.
4. Implement a first-pass team-fit heuristic.
5. On priority pages, show likely owner suggestions and a short explanation.
6. Keep the heuristic simple and easy to inspect in code.

Acceptance check for Phase 6:

- Person notes load and render correctly.
- Priority pages show understandable staffing suggestions.

### Phase 7: Implement Cycle Views And Briefs

1. Build `/cycles` list view.
2. Build `/cycles/:id` detail view.
3. Show related priorities by matching each priority's `cycle` field.
4. Show the cycle note narrative sections.
5. Add a current-brief view if time allows.
6. The brief should answer:
   - what we are focusing on
   - why these priorities matter now
   - likely staffing direction
   - known risks and tradeoffs

Acceptance check for Phase 7:

- A cycle page reads like a useful communication artifact.
- Related priorities appear correctly.

### Phase 8: Polish Without Expanding Scope

1. Improve empty states.
2. Improve form defaults.
3. Improve readability of comparison tables.
4. Add small progressive enhancements with vanilla JS only if clearly useful.
5. Keep startup fast and code simple.
6. Do not add major dependencies during polish.

Acceptance check for Phase 8:

- The app feels calm and usable.
- The codebase remains small.
- Raw files still look excellent outside the app.

## Implementation Notes

- Use plain HTML forms and full-page post/redirect/get flows.
- Avoid client-heavy state management.
- Prefer simple server-rendered pages first.
- Keep all file writes explicit and safe.
- Make error messages human-readable.
- Use stable slugs for note IDs.
- Favor predictable code over clever abstractions.

## Suggested Initial Templates

Create starter templates in `content/templates` using the exact note shapes in this guide.

- `priority.md`
- `person.md`
- `cycle.md`

These templates should be used by the create flows.

## Manual Verification Checklist

Before handing work back to the user, verify:

- the app starts locally
- the sample content loads
- create/edit flows work
- Markdown rendering works
- comparison formulas work
- team-fit suggestions appear
- cycle pages show related priorities
- raw Markdown files remain clean and readable

## Future Packaging Direction

Not now, but design for it.

- Keep business logic independent from the current dev server shape.
- Keep filesystem access centralized.
- Keep the app local-first.
- Later, this can be wrapped as a desktop app, likely with a lightweight wrapper such as Tauri if the user still wants that.
- Do not start packaging work until the user asks.

## Final Reminder To The Next Agent

- Start with scaffolding and the content layer.
- Do not skip the schema work.
- Do not add unnecessary dependencies.
- Do not drift into Agile/task-tracker features.
- Do not replace Markdown with a database.
- Build the smallest thing that feels durable, thoughtful, and Obsidian-adjacent.
