# Simulation First Implementation Plan

## Purpose

This plan defines the first implementation pass for the Jefferson Mark III simulation engine. It is scoped to the deterministic engine spine and a narrow rules subset. It does not attempt the full scenario suite, rich Mesa agents, or complete Charter simulation.

The implementation shall use `docs/simulation/requirements/index.md` as the requirements source and `docs/simulation_design.md` as the design guide.

## Phase 0 - Environment And Test Harness

Goal: make the simulation package installable and testable.

Deliverables:

- `simulation/pyproject.toml` or equivalent test configuration if needed.
- Test discovery under `simulation/tests/`.
- Importable package under `simulation/src/jefferson_sim/`.
- `.venv`-friendly workflow using root `requirements.txt`.

Verification:

- `pytest simulation/tests` runs.
- A trivial package import test passes.

## Phase 1 - Core Records And State

Goal: implement the data model spine without rule complexity.

Deliverables:

- Dataclass records for Subscriber, Representative, Delegation, Authority, Authority Charter, Scope, Approval Record, Simulation Event, Rule Decision, Metric Record.
- Enum values for event status and Authority lifecycle state.
- `SimulationState` container with dictionaries keyed by stable IDs.
- Serialization helpers for JSON-compatible output.

Requirements focus:

- `SIM-REQ-500` through `SIM-REQ-518`
- `SIM-REQ-530` through `SIM-REQ-539`
- `SIM-REQ-550`

Verification:

- Record schema tests.
- Required-field validation tests.
- JSON serialization tests.

## Phase 2 - Configuration And Validation

Goal: load Charter derivative and scenario inputs with clear validation errors.

Deliverables:

- YAML loader for `derivatives/simulation/charter_sim.yaml`.
- Minimal scenario loader for YAML or JSON.
- Validation report model.
- Gap assumption validation.
- Rule traceability metadata validation.

Requirements focus:

- `SIM-REQ-010` through `SIM-REQ-020D`
- `SIM-REQ-230` through `SIM-REQ-248`
- `SIM-REQ-257`

Verification:

- Valid config loads.
- Missing required fields fail validation.
- Unresolved gap assumptions fail when required but undeclared.
- Simulation abstraction notices are emitted.

## Phase 3 - Event Pipeline And Replay Spine

Goal: process events deterministically and produce auditable logs.

Deliverables:

- Stable event ID assignment.
- Event validation.
- Deterministic same-tick ordering policy.
- Rule decision log.
- No-op decision handling.
- State hash after each tick.

Requirements focus:

- `SIM-REQ-512` through `SIM-REQ-518`
- `SIM-REQ-520` through `SIM-REQ-527`
- `SIM-REQ-250` through `SIM-REQ-263`

Verification:

- Same scenario and seed produce same final state hash.
- Invalid events appear in validation/errors output.
- Event logs include accepted and rejected events.

## Phase 4 - Narrow Rule Subset

Goal: implement enough Charter mechanics to make the engine meaningful before Mesa integration.

Deliverables:

- Approval threshold evaluation from Approval Records.
- Authority lifecycle state machine.
- Basic Authority formation pass/fail.
- Delegation creation/revocation/activation scheduling.
- Raw delegation aggregation.
- Basic metric formulas for raw concentration, delegation churn, Authority count, and lifecycle outcomes.

Requirements focus:

- `SIM-REQ-110` through `SIM-REQ-129`, except weighted delegation details blocked by gaps.
- `SIM-REQ-130` through `SIM-REQ-149`
- `SIM-REQ-550` through `SIM-REQ-568`
- `SIM-REQ-270`, `SIM-REQ-272`, `SIM-REQ-273`, `SIM-REQ-282`, `SIM-REQ-283`
- `SIM-REQ-590`, `SIM-REQ-593`, `SIM-REQ-594`, `SIM-REQ-605`

Verification:

- Delegation lifecycle tests.
- Authority formation and rejection tests.
- Invalid lifecycle transition tests.
- Metric formula tests.

## Phase 5 - Output Artifacts

Goal: write first-pass run artifacts locally.

Deliverables:

- `manifest.json`
- `validation_report.json`
- `event_log.jsonl`
- `rule_decisions.jsonl`
- `metrics_summary.json`
- `time_series.csv`
- `final_state.json`

Requirements focus:

- `SIM-REQ-290` through `SIM-REQ-301`

Verification:

- Each artifact is emitted for a valid minimal scenario.
- Output artifacts contain enough provenance for replay.
- Final state includes core state records.

## Phase 6 - Minimal Scenario Acceptance

Goal: prove the engine spine with one narrow scenario.

Deliverables:

- Minimal Basic Delegation Stability scenario.
- Minimal Authority Creation scenario.

Requirements focus:

- `SIM-REQ-310` through `SIM-REQ-313`

Verification:

- Scenarios run deterministically.
- Expected events, decisions, and metrics appear.

## Explicitly Deferred From First Pass

The first implementation pass shall not include:

- Full Mesa adapter.
- Rich Subscriber, Representative, Authority, adversarial, court, or event-generator agents.
- Weighted delegation unless assumptions are explicitly configured.
- Full scope conflict detection.
- Emergency lifecycle beyond data model stubs.
- Consolidation audits and CCA decisions.
- Satisfaction-driven behavior beyond storage and abstraction notices.
- Full starter scenario suite.

Deferred items are tracked in `docs/simulation_gaps.md`.

## Definition Of Done

The first implementation pass is complete when:

- The core engine package imports.
- Unit tests pass for implemented records, validation, event processing, lifecycle, approval, delegation, and output artifacts.
- A minimal delegation scenario runs deterministically.
- A minimal Authority formation scenario runs deterministically.
- All skipped requirements are listed in `docs/simulation_gaps.md`.
