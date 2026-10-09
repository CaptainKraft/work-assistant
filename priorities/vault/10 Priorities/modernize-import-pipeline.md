---
id: modernize-import-pipeline
title: Modernize import pipeline
type: priority
status: backlog
tags:
  - interop
  - pipeline
  - import
owners:
  - "[[emma]]"
  - "[[ben]]"
cycle:
appetite: 6 weeks
strategic_alignment: 4
confidence: 2
team_fit: 4
rice_reach: 3
rice_impact: 4
rice_confidence: 2
rice_effort: 4
ice_impact: 4
ice_confidence: 2
ice_ease: 2
delay_cost: 3
delay_effort: 4
selected: false
---

## Problem

Import behavior has grown uneven over time, which makes some customer workflows harder to trust and harder for the team to debug.

## Why Now

The pain is real, but the shape is still too broad. This note exists to capture the opportunity before it gets flattened into vague "pipeline work."

## Desired Outcome

Clarify the import path, reduce avoidable confusion, and make edge cases easier to diagnose.

## Boundaries

- focus on the highest-friction import path first
- avoid a full system rewrite
- treat better diagnostics as part of the outcome, not a separate cleanup task

## Risks

- the term "modernize" hides too much possible scope
- migration concerns could expand quickly once implementation starts
- [ ] identify the exact import path to target before moving this to `todo`

## Staffing Notes

[[emma]] is the strongest owner because she understands import reality in production. [[ben]] is useful if tooling or workflow cleanup becomes part of the bet.

## Decision Rationale

This remains in backlog because the opportunity is important but not yet shaped tightly enough. It is a good test case for whether Obsidian notes help clarify broad ideas before they become real bets.
