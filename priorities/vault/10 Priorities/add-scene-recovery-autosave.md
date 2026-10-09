---
id: add-scene-recovery-autosave
title: Add scene recovery autosave
type: priority
status: cancelled
tags:
  - reliability
  - autosave
  - recovery
owners:
  - "[[felix]]"
  - "[[emma]]"
cycle: "[[2026-cycle-2]]"
appetite: 6 weeks
strategic_alignment: 4
confidence: 2
team_fit: 3
rice_reach: 4
rice_impact: 4
rice_confidence: 2
rice_effort: 5
ice_impact: 4
ice_confidence: 2
ice_ease: 1
delay_cost: 4
delay_effort: 5
selected: false
---

## Problem

Artists can lose meaningful work after a crash or forced close. Recovery is one of those pains everyone understands immediately.

## Why Now

The opportunity came up during shaping for the current cycle, but the more we looked at it, the wider the surface area became.

## Desired Outcome

Provide a safe recovery path for active scene work after an unexpected interruption.

## Boundaries

- focus on recovery files for active scenes only
- avoid expanding into cloud sync, version history, or collaborative recovery
- keep performance and data integrity constraints explicit

## Risks

- file integrity and corruption risk are non-trivial
- the operational edge cases multiply quickly
- [ ] revisit only after a smaller shape is defined

## Staffing Notes

[[felix]] and [[emma]] were plausible owners, but the bet needed tighter boundaries before staffing it confidently.

## Decision Rationale

This was cancelled for the current cycle because the appetite no longer matched the real scope. The note should stay as a record of the tradeoff, not as a silent disappearance.
