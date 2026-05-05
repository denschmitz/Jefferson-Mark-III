# Simulation Design

## Purpose

This document describes the first-pass implementation design for the Jefferson Mark III simulation engine. It does not replace `docs/simulation/requirements/index.md`; it organizes a practical implementation that can satisfy those requirements with conservative scope.

The design goal is a deterministic Charter mechanics engine with a thin Mesa adapter. Charter rule evaluation stays independent from Mesa so it can be unit tested directly.

## Module Boundaries

```text
simulation/src/jefferson_sim/
├── engine/
│   ├── config.py
│   ├── state.py
│   ├── records.py
│   ├── rules.py
│   ├── approvals.py
│   ├── lifecycle.py
│   ├── conflicts.py
│   ├── events.py
│   ├── metrics.py
│   ├── validation.py
│   └── runner.py
└── mesa_adapter/
    ├── model.py
    ├── agents.py
    ├── schedule.py
    └── collectors.py
```

`engine/` owns Charter mechanics, validation, state transitions, metrics, and output artifacts.

`mesa_adapter/` owns Mesa `Model` and `Agent` integration. It creates agents, advances steps, and forwards agent events into the engine. It does not duplicate Charter rule logic.

## Data Model Choices

Use plain Python dataclasses for first pass records:

- `SubscriberRecord`
- `RepresentativeRecord`
- `DelegationRecord`
- `AuthorityRecord`
- `AuthorityCharterRecord`
- `ScopeRecord`
- `ApprovalRecord`
- `SimulationEvent`
- `RuleDecision`
- `MetricRecord`

Dataclasses are sufficient for deterministic state, serialization, and tests without introducing ORM or database complexity. Validation should happen at load and event-processing boundaries.

Use dictionaries keyed by stable IDs inside `SimulationState`:

- `subscribers: dict[str, SubscriberRecord]`
- `representatives: dict[str, RepresentativeRecord]`
- `delegations: dict[str, DelegationRecord]`
- `authorities: dict[str, AuthorityRecord]`
- `scopes: dict[str, ScopeRecord]`
- `events: dict[str, SimulationEvent]`

## Rule Engine Architecture

The rule engine should be a pure Python service layer around immutable or controlled state transitions.

Primary components:

- `RuleRegistry`: maps `rule_id` to rule metadata, Charter traceability, and callable rule function.
- `EventProcessor`: receives events, orders them, invokes rules, and writes decisions.
- `SimulationState`: holds current records and append-only logs.
- `ValidationService`: validates config, records, assumptions, and event payloads.
- `MetricsService`: calculates per-tick and run-summary metrics from state and event logs.

Rule functions should accept state plus event payload and return a `RuleDecision` plus optional state changes. They should not perform file I/O.

## Event Processing Pipeline

First-pass tick flow:

1. Load scenario and Charter derivative.
2. Validate scenario, assumptions, initial state, and rule traceability.
3. Initialize `SimulationState`.
4. For each tick:
   - collect scheduled scenario events;
   - collect Mesa agent events if running through Mesa;
   - assign stable event IDs;
   - validate event schemas;
   - sort by `effective_tick` and deterministic priority;
   - process events through the rule registry;
   - append rule decisions and lifecycle transitions;
   - recalculate derived totals;
   - calculate per-tick metrics;
   - compute state hash.
5. Emit final artifacts.

Invalid events should be preserved in the validation/errors report with rejection reasons.

## Validation Flow

Validation should run in layers:

1. **File validation**: YAML/JSON parse, required top-level fields, schema version.
2. **Charter derivative validation**: required rule sections, derivative metadata, known gap declarations.
3. **Scenario validation**: seed, duration, agents, initial records, enabled abstractions, assumptions.
4. **State validation**: token conservation, required IDs, Authority-charter links, lifecycle state values.
5. **Event validation**: known event type, required payload fields, actor/target references.
6. **Rule validation**: rule has Charter traceability or abstraction metadata.

Blocking validation errors prevent the run. Warnings and abstraction notices are emitted into the validation report.

## Persistence And Output Format

Use local file outputs for first pass. No database is required.

Recommended output directory:

```text
simulation/runs/<scenario_id>/<run_id>/
├── manifest.json
├── validation_report.json
├── event_log.jsonl
├── rule_decisions.jsonl
├── metrics_summary.json
├── time_series.csv
└── final_state.json
```

Use JSON Lines for event and decision logs because append-only records are easy to inspect and diff. Use JSON for structured manifests and final state. Use CSV for per-tick time series because it is easy to plot.

## Mesa Integration

Mesa plugs in at the event generation and stepping boundary.

`CharterMesaModel` should:

- hold a reference to `SimulationRunner` or `EventProcessor`;
- create Mesa agents from scenario config;
- call agent step methods;
- collect emitted events;
- submit events to the engine for the current tick;
- expose collected metrics for Mesa-compatible analysis or visualization.

Mesa agents should not mutate engine state directly. They emit events. The engine accepts, rejects, or transforms those events through rule decisions.

## Dependency Choices

First-pass dependencies:

- `mesa`: agent-based runtime and optional visualization support.
- `PyYAML`: load Charter derivative and YAML scenario files.
- `pytest`: unit and scenario tests.

Recommended standard library use:

- `dataclasses` for records.
- `enum` for lifecycle states and event statuses.
- `json` and `csv` for outputs.
- `hashlib` for state and input hashes.
- `random.Random` for deterministic seeded randomness.
- `pathlib` for filesystem paths.

Avoid first-pass dependencies on database libraries, web frameworks, pandas, or validation frameworks unless requirements become too expensive to satisfy with small local validators.

## Test Strategy

Use tests in layers:

- **Record tests**: required fields, invalid values, serialization.
- **Validation tests**: missing scenario fields, unresolved gaps, invalid event types.
- **Rule tests**: thresholds, delegation limits, lifecycle transitions, emergency deadlines, scope conflicts.
- **Metric tests**: formula outputs and edge cases.
- **Replay tests**: same scenario and seed produce same final state hash.
- **Mesa adapter tests**: agents emit events and call engine services without duplicating rule logic.
- **Scenario acceptance tests**: starter scenarios satisfy expected metrics and event outcomes.

Pure engine tests should not import Mesa. Mesa adapter tests may import Mesa.

## Known Tradeoffs

- Dataclasses are less strict than a schema library, but they keep first-pass complexity low.
- JSON/JSONL outputs are not optimized for large simulations, but they are transparent and easy to audit.
- Structural scope conflict detection avoids natural-language interpretation, but it requires scenario authors to encode scope fields carefully.
- Satisfaction and adversarial behavior remain simulation abstractions until the Charter defines more mechanics.
- Keeping Mesa thin reduces duplication, but it means Mesa agents are event generators rather than fully autonomous holders of constitutional logic.
- A deterministic event pipeline may feel artificial for political behavior, but it is necessary for reproducible stress testing.

## Implementation Order

1. Define dataclasses and state container.
2. Load and validate `charter_sim.yaml`.
3. Load and validate scenario files.
4. Implement event log, rule decision log, and state hashing.
5. Implement delegation and approval rules.
6. Implement Authority lifecycle state machine.
7. Implement emergency timing rules.
8. Implement structural scope conflict detection.
9. Implement metrics and output artifacts.
10. Add Mesa model and agent adapter.
