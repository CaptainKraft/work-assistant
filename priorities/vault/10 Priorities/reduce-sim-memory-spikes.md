---
id: reduce-sim-memory-spikes
title: Reduce simulation memory spikes
type: priority
status: backlog
tags:
  - simulation
  - performance
  - stability
owners:
  - "[[devon]]"
  - "[[alice]]"
cycle:
appetite: 5 weeks
strategic_alignment: 4
confidence: 3
team_fit: 4
rice_reach: 3
rice_impact: 4
rice_confidence: 3
rice_effort: 4
ice_impact: 4
ice_confidence: 3
ice_ease: 2
delay_cost: 4
delay_effort: 4
selected: false
---

## Problem

Some heavy simulations still produce memory spikes that make machines unstable or force users into uncomfortable workarounds.

## Why Now

The pain matters, especially for larger customers, but the technical path is riskier and less bounded than the current cycle bets.

## Desired Outcome

Smooth out the worst memory behavior enough that users see fewer catastrophic spikes and have better guardrails before they hit system limits.

## Boundaries

- focus on a narrow slice of the worst cases first
- avoid turning this into a full solver or memory architecture rewrite
- keep user-visible validation part of the bet

## Risks

- a meaningful fix may require deeper architectural change than the appetite allows
- performance gains could be scenario-specific and hard to communicate clearly
- [ ] identify one representative problem case before prioritizing this higher

## Staffing Notes

[[devon]] is the obvious technical lead. [[alice]] is a plausible partner if graphics-side memory behavior or cross-system tradeoffs matter.

## Decision Rationale

This is important, but it remains a later candidate because the risk of scope growth is still high. It is a good note to revisit after the current reliability work yields more insight.
