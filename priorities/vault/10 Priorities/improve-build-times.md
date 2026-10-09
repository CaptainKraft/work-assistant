---
id: improve-build-times
title: Improve build times
type: priority
status: todo
tags:
  - tooling
  - developer-experience
  - build
owners:
  - "[[ben]]"
  - "[[emma]]"
cycle:
appetite: 2 weeks
strategic_alignment: 3
confidence: 5
team_fit: 5
rice_reach: 2
rice_impact: 4
rice_confidence: 5
rice_effort: 1
ice_impact: 4
ice_confidence: 5
ice_ease: 5
delay_cost: 2
delay_effort: 1
selected: false
---

## Problem

Local build iteration is still slower than it should be after common engine-side changes. The drag is internal, but it compounds every day.

## Why Now

This is a strong leverage bet with very high confidence. It competes poorly against customer-visible work only because the current cycle already has a clear external focus.

## Desired Outcome

Cut common local iteration times enough that engineers feel the improvement every week without changing how they work.

## Boundaries

- focus on the most common slow path first
- do not turn this into a full build-system migration
- keep measurements concrete and easy to communicate

## Risks

- optimizing the wrong path could produce a "win" nobody feels
- infrastructure improvements can keep expanding if not held to a small appetite
- [ ] decide whether this should be pulled into the current cycle as a small leverage bet

## Staffing Notes

[[ben]] is the natural lead. [[emma]] is a useful second owner if repro and measurement discipline are needed.

## Decision Rationale

This sits in `todo` because it is well understood and valuable, but not yet selected for the active cycle. It is a good example of a high-confidence bet that may still lose on strategic timing.
