---
id: improve-error-messages-in-export
title: Improve error messages in export
type: priority
status: done
tags:
  - export
  - ux
  - diagnostics
owners:
  - "[[emma]]"
  - "[[claire]]"
cycle: "[[2026-cycle-1]]"
appetite: 2 weeks
strategic_alignment: 4
confidence: 4
team_fit: 5
rice_reach: 4
rice_impact: 4
rice_confidence: 4
rice_effort: 1
ice_impact: 4
ice_confidence: 4
ice_ease: 5
delay_cost: 3
delay_effort: 1
selected: true
---

## Problem

When export failed, users often got too little context to act on. That created repeated support churn and made the product feel more mysterious than it needed to.

## Why Now

This was a good prior-cycle bet because it was small, highly leveraged, and clearly tied to support pain.

## Desired Outcome

Show more actionable errors, clearer next steps, and better links between product behavior and user understanding.

## Boundaries

- improve messages and immediate diagnostics only
- avoid rebuilding the exporter architecture as part of this work
- keep the changes visible and testable in real failure paths

## Risks

- wording improvements alone might hide deeper product issues
- [x] verify that support can resolve common failures faster with the new messages

## Staffing Notes

[[emma]] handled the technical realities while [[claire]] helped make the messages genuinely useful to users.

## Decision Rationale

This is a useful example of a small bet with high leverage. It improved support outcomes and user clarity without requiring a broader rewrite.
