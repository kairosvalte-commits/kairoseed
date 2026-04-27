# Evaluation Protocol for Kairoseed v0.4

This document defines the evaluation layer for Kairoseed, separating validation logic from the published system overview.

## Purpose

The evaluation protocol describes:
- A/B/C test categories for system validation
- scoring validation rules for GSBS
- memory drift measurement methods
- evolution success criteria for PEE

This protocol is intended for research-grade documentation and experiment reproducibility.

## A / B / C Test Categories

### A: Scoring Validation
A tests verify the GSBS scoring system and decision selection logic.

Key checks:
- each hypothesis receives a score object with all four components: `success`, `stability`, `cost`, `risk`
- raw component values are normalized in the expected range [0.0, 1.0]
- weight vectors maintain a valid distribution, with weights summing to 1.0
- selection chooses the hypothesis with the highest weighted utility while respecting risk and quality thresholds

### B: Memory Drift Validation
B tests measure whether the memory system preserves stable adaptation and avoids runaway drift.

Key methods:
- capture a baseline memory state at the start of an experiment
- compute drift as the mean absolute change across the four evaluation dimensions:
  - `success`
  - `stability`
  - `cost`
  - `risk`
- report drift as:
  - `drift = mean(|latest - baseline|)`
  - `direction = improving | declining | stable`

A stable memory-feedback experiment should show bounded drift and, when successful, an `improving` direction.

### C: Evolution Success Criteria
C tests define whether hypothesis evolution produces consistent improvement and convergence behavior.

Success criteria include:
- the evolved population size remains within configured bounds after pruning
- the selected hypothesis score is greater than or equal to the previous selection score
- stability is preserved or improves across iterations, avoiding solutions that improve success only by sacrificing stability
- memory updates reflect actual outcome feedback rather than arbitrary oscillation

## Benchmark Execution Layer

Kairoseed is validated through three core benchmark classes:

### 1. Stability Benchmark
Measures whether identical inputs produce identical decisions.

### 2. Memory Drift Benchmark
Measures whether memory updates induce behavioral divergence over repeated runs.

### 3. Evolution Gain Benchmark
Measures whether PEE produces measurable improvement in hypothesis scoring.

All benchmarks operate on identical input states and isolate system behavior across runs.

## Scoring Validation Rules

1. `Score(H_i)` is computed from the weighted vector:
   - `Score(H_i) = w_success * Success + w_stability * Stability - w_cost * Cost - w_risk * Risk`
2. All score components must be in [0.0, 1.0].
3. Weight components must satisfy:
   - `w_success + w_stability + w_cost + w_risk = 1.0`
   - each weight in [0.0, 1.0]
4. Selected hypothesis must maximize the weighted score while satisfying the configured thresholds for risk and minimum acceptance quality.
5. Validation routines should flag missing or malformed score vectors, invalid weights, and selection decisions that violate constraints.

## Memory Drift Measurement Method

The memory drift measurement method uses recorded evaluation history across iterations.

Procedure:
1. record the baseline metrics at experiment start: `baseline = history[0]`
2. record the latest metrics at experiment end: `latest = history[-1]`
3. compute average drift across four dimensions:
   - `drift = (|latest.success - baseline.success| + |latest.stability - baseline.stability| + |latest.cost - baseline.cost| + |latest.risk - baseline.risk|) / 4`
4. infer direction based on `success` change:
   - `improving` if `latest.success >= baseline.success`
   - `declining` otherwise
5. use drift and direction to assess whether the memory system is stable, reverting, or improving.

Notes:
- bounded drift is expected for a mature research system.
- uncontrolled drift indicates unstable memory-feedback conditions.

## Evolution Success Criteria

The evolution protocol should be judged using both local and long-term metrics.

Criteria:
- `score_improvement`: the selected hypothesis score should not decline sharply between iterations
- `stability_preservation`: the chosen solution should maintain or improve stability
- `population_health`: the evolved set should retain a diverse but high-quality population, with no excessive pruning
- `memory_feedback_alignment`: memory updates should align predicted outcomes with actual outcomes rather than creating divergent internal bias

A successful evolution cycle is one where score and stability improve together and drift remains bounded.

## Research Status

This evaluation protocol clarifies the current research scope: Kairoseed is a prototype system with documented evaluation boundaries, not a guarantee of global optimality.

For implementation details and system architecture, see the core documentation in `docs/architecture_v0.4.md` and `docs/system_spec.md`.
