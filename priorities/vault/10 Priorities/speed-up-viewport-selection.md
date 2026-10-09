---
id: speed-up-viewport-selection
title: Speed up viewport selection
type: priority
status: todo
tags:
  - viewport
  - interaction
  - performance
owners:
  - "[[felix]]"
  - "[[alice]]"
cycle: "[[2026-cycle-2]]"
appetite: 3 weeks
strategic_alignment: 4
confidence: 4
team_fit: 5
rice_reach: 4
rice_impact: 4
rice_confidence: 4
rice_effort: 2
ice_impact: 4
ice_confidence: 4
ice_ease: 4
delay_cost: 3
delay_effort: 2
selected: true
---

## Problem

Selection in dense scenes still feels too slow and uncertain. Artists notice it immediately because it sits in a hot path that should feel effortless.

## Why Now

The pain is active, specific, and contained. It is a good example of a bet that improves the daily feel of the product without demanding a broad platform rewrite.

## Desired Outcome

Make selection in representative heavy scenes feel responsive again. The target is a noticeable improvement in confidence and interaction speed, not a full viewport overhaul.

## Boundaries

- focus on hit testing, selection queries, and user-visible response time
- avoid widening the bet into a complete viewport performance pass
- preserve room for follow-on work if deeper architecture issues appear

## Risks

- there may be hidden coupling with scene graph behavior
- apparent selection lag may come from multiple smaller bottlenecks
- [ ] capture a before/after benchmark scene for comparison

## Staffing Notes

[[felix]] is the strongest owner because the problem sits in editor feel and viewport behavior. [[alice]] is a good partner for graphics-side validation and performance tradeoffs.

## Decision Rationale

This is in the current cycle because it is a bounded, high-trust improvement with excellent team fit. It also gives the team a concrete user-facing win without sprawling scope.
