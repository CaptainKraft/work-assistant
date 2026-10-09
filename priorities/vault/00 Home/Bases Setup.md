This note describes the Bases to create manually in Obsidian.

## Source folder

Point each priority Base at `10 Priorities/` and filter for `type = priority`.

## Recommended priority Bases

### Backlog

- filter: `status = backlog`
- sort: `strategic_alignment desc`, then `confidence desc`
- fields: `title`, `status`, `appetite`, `owners`, `strategic_alignment`, `confidence`, `team_fit`

### Todo

- filter: `status = todo`
- sort: `selected desc`, then `strategic_alignment desc`
- fields: `title`, `cycle`, `appetite`, `owners`, `selected`, `strategic_alignment`, `confidence`, `team_fit`

### Working

- filter: `status = working`
- fields: `title`, `cycle`, `owners`, `appetite`, `confidence`, `team_fit`

### Current Cycle

- filter: `cycle contains [[2026-cycle-2]]
- sort: `status asc`, then `title asc`
- fields: `title`, `status`, `owners`, `appetite`, `selected`, `strategic_alignment`, `confidence`, `team_fit`

### Compare Candidates

- filter: `status in [backlog, todo]`
- sort: `strategic_alignment desc`, then `rice_score desc`
- fields:
  - `title`
  - `status`
  - `cycle`
  - `appetite`
  - `owners`
  - `strategic_alignment`
  - `confidence`
  - `team_fit`
  - `rice_score`
  - `ice_score`
  - `delay_effort_score`
  - `selected`

### Done

- filter: `status = done`
- sort: `cycle desc`
- fields: `title`, `cycle`, `owners`, `appetite`, `strategic_alignment`, `confidence`, `team_fit`

### Cancelled

- filter: `status = cancelled`
- fields: `title`, `cycle`, `appetite`, `owners`, `selected`
- use the note body to review the `Decision Rationale` section when discussing why an item was stopped

## People Base

Create a second Base pointed at `20 People/`.

- fields: `name`, `role`, `strengths`, `interests`, `domains`, `load`, `tags`
- useful groupings: by `load` or by `domains`

## Suggested formulas

If your version of Bases supports formulas comfortably, add:

- `rice_score = (rice_reach * rice_impact * rice_confidence) / rice_effort`
- `ice_score = ice_impact * ice_confidence * ice_ease`
- `delay_effort_score = delay_cost / delay_effort`

If formula support feels clunky, keep the raw inputs visible and calculate the scores manually when comparing only a few candidates.
