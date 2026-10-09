---
id: reduce-crash-reports
title: Reduce crash reports
type: priority
status: working
tags:
  - stability
  - reliability
  - performance
owners:
  - "[[devon]]"
  - "[[emma]]"
cycle: "[[2026-cycle-2]]"
appetite: 6 weeks
strategic_alignment: 5
confidence: 3
team_fit: 5
rice_reach: 4
rice_impact: 5
rice_confidence: 3
rice_effort: 4
ice_impact: 5
ice_confidence: 3
ice_ease: 2
delay_cost: 5
delay_effort: 4
selected: true
---

## Problem

Too many support conversations still start with a crash instead of a product outcome. The top signatures are well-known, but they have not been treated as a focused reliability bet.

## Why Now

Reliability is part of the product promise. If trust in the product drops, every other improvement becomes harder to feel or defend.

## Desired Outcome

Reduce the top crash signatures meaningfully enough that support and production users both notice the improvement. The goal is fewer repeated failures, not a marketing-perfect crash number.

## Boundaries

- focus on the highest-frequency signatures first
- improve repro coverage and instrumentation where it helps the bet stay tractable
- do not turn this into a general crash backlog cleanup effort

## Risks

- hidden driver or environment issues may limit how much progress is visible
- crash fixes may reveal deeper architecture problems than the appetite allows
- [ ] keep the work framed around a short list of signatures

## Staffing Notes

[[devon]] is the clear technical lead. [[emma]] is important for building reproducible cases and keeping the work grounded in support reality.

## Decision Rationale

This bet is less flashy than some product-facing work, but it is central to trust. It stays in cycle because the pain is real, repeated, and well enough understood to pursue as a bounded reliability push.
